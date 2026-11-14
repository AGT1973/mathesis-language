#!/usr/bin/env python3
r"""
E:\MATHESIS\tests\test_compare_cpp_vs_mathesis2bin.py
=====================================================
Kit de pruebas comparativo SOTA en silicio real (Ghost Protocol):
  - Camino Humano (C++20 MSVC /O2 /arch:AVX): atelier_stiefel_cpp.exe
  - Camino Directo (Espacio Vectorial -> PE64 SSE2): atelier_stiefel_mathesis2bin.exe
"""

import os
import sys
import struct
import subprocess
import statistics
import time
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import pytest

sys.path.insert(0, r"E:\MATHESIS\src")
from mathesis2bin import DirectX64PEBuilder

CPP_EXE = r"E:\github_gitlab\workspaces\POLYDIM_EinSof\tools\atelier_kernel\atelier_stiefel_cpp.exe"
M2B_EXE = r"E:\MATHESIS\bin\atelier_stiefel_mathesis2bin.exe"


def _parse_pe64(path: str) -> dict:
    with open(path, "rb") as f:
        data = f.read()
    assert data[:2] == b"MZ", f"No es PE válido: {path}"
    e_lfanew = struct.unpack_from("<I", data, 60)[0]
    assert data[e_lfanew : e_lfanew + 4] == b"PE\x00\x00"
    machine, num_sections = struct.unpack_from("<HH", data, e_lfanew + 4)
    opt_size = struct.unpack_from("<H", data, e_lfanew + 20)[0]
    sec_off = e_lfanew + 24 + opt_size
    sections = {}
    for i in range(num_sections):
        off = sec_off + i * 40
        name = data[off : off + 8].rstrip(b"\x00").decode("ascii", errors="replace")
        vsize, rva, rsize = struct.unpack_from("<III", data, off + 8)
        sections[name] = {"vsize": vsize, "rva": rva, "rsize": rsize}
    return {
        "file_bytes": len(data),
        "machine": hex(machine),
        "num_sections": num_sections,
        "sections": sections,
        "raw": data,
    }


def _percentile(sorted_vals: list, p: float) -> float:
    idx = min(len(sorted_vals) - 1, max(0, int(round((p / 100.0) * (len(sorted_vals) - 1)))))
    return sorted_vals[idx]


def _run_bench(path: str, runs: int = 20, warmup: int = 2, cwd: str | None = None) -> dict:
    for _ in range(warmup):
        r = subprocess.run([path], cwd=cwd, capture_output=True, text=True)
        assert r.returncode == 0
    lat = []
    last_out = ""
    for _ in range(runs):
        t0 = time.perf_counter()
        r = subprocess.run([path], cwd=cwd, capture_output=True, text=True)
        dt = (time.perf_counter() - t0) * 1000.0
        assert r.returncode == 0, f"Falló {path}: {r.stderr}"
        lat.append(dt)
        last_out = r.stdout
    lat.sort()
    return {
        "runs": runs,
        "min_ms": lat[0],
        "p50_ms": statistics.median(lat),
        "mean_ms": statistics.mean(lat),
        "p95_ms": _percentile(lat, 95),
        "max_ms": lat[-1],
        "stdev_ms": statistics.stdev(lat),
        "stdout": last_out,
    }


def test_01_executables_and_pe64_headers():
    assert os.path.isfile(CPP_EXE), f"Falta {CPP_EXE}"
    assert os.path.isfile(M2B_EXE), f"Falta {M2B_EXE}"
    cpp_pe = _parse_pe64(CPP_EXE)
    m2b_pe = _parse_pe64(M2B_EXE)
    assert cpp_pe["machine"] == "0x8664"
    assert m2b_pe["machine"] == "0x8664"
    assert m2b_pe["num_sections"] == 3


def test_02_code_footprint_comparison():
    cpp_pe = _parse_pe64(CPP_EXE)
    m2b_pe = _parse_pe64(M2B_EXE)
    cpp_text = cpp_pe["sections"][".text"]["vsize"]
    m2b_text = m2b_pe["sections"][".text"]["vsize"]
    assert m2b_text < 512
    assert m2b_pe["file_bytes"] < cpp_pe["file_bytes"]
    ratio = cpp_text / m2b_text
    print(
        f"\n[FOOTPRINT] C++20 .text={cpp_text}B (total={cpp_pe['file_bytes']}B) "
        f"| mathesis2bin .text={m2b_text}B (total={m2b_pe['file_bytes']}B) | Ratio={ratio:.1f}x"
    )


def test_03_numerical_invariance_both_executables(tmp_path):
    # 1) C++20 MSVC QDWH
    cpp_slab = tmp_path / "cpp_st_16_1024.bin"
    r_cpp = subprocess.run([CPP_EXE, "1024", "16", "--dump-slab-file", str(cpp_slab)], capture_output=True, text=True)
    assert r_cpp.returncode == 0
    raw_cpp = cpp_slab.read_bytes()
    assert len(raw_cpp) >= 64 + 16 * 1024 * 8
    W_cpp = np.frombuffer(raw_cpp[64 : 64 + 16 * 1024 * 8], dtype=np.float64).reshape(1024, 16)
    err_cpp = float(np.max(np.abs(W_cpp.T @ W_cpp - np.eye(16))))
    assert err_cpp <= 1e-15, f"Defecto C++20 excede cota: {err_cpp}"

    # 2) mathesis2bin Direct PE64 SSE2 MGS
    r_m2b = subprocess.run([M2B_EXE], cwd=str(tmp_path), capture_output=True, text=True)
    assert r_m2b.returncode == 0
    m2b_slab = tmp_path / "m2b_slab.bin"
    assert m2b_slab.is_file(), "mathesis2bin no exportó m2b_slab.bin"
    W_m2b = np.fromfile(str(m2b_slab), dtype=np.float64).reshape(16, 1024)
    err_m2b = float(np.max(np.abs(W_m2b @ W_m2b.T - np.eye(16))))
    assert err_m2b <= 1e-15, f"Defecto mathesis2bin excede cota: {err_m2b}"

    print(f"\n[INVARIANZA DUAL St(16,1024)] C++20_QDWH={err_cpp:.2e} | M2B_MGS_SSE2={err_m2b:.2e}")


def test_04_mathesis2bin_multi_dimension_emit_and_run(tmp_path):
    configs = [(8, 256), (16, 1024), (32, 2048)]
    results = []
    for k, d in configs:
        out_exe = str(tmp_path / f"m2b_{k}_{d}.exe")
        t0 = time.perf_counter()
        info = DirectX64PEBuilder(k=k, d=d).build_pe64(out_exe)
        emit_ms = (time.perf_counter() - t0) * 1000.0
        r = subprocess.run([out_exe], cwd=str(tmp_path), capture_output=True, text=True)
        assert r.returncode == 0, f"Fallo St({k},{d})"
        W = np.fromfile(str(tmp_path / "m2b_slab.bin"), dtype=np.float64).reshape(k, d)
        err = float(np.max(np.abs(W @ W.T - np.eye(k))))
        assert err <= 1e-14, f"Error St({k},{d})={err}"
        results.append(f"St({k},{d}): emit={emit_ms:.1f}ms size={info['file_bytes']}B err={err:.2e}")
    print("\n[MULTI-DIM M2B] " + " | ".join(results))


def test_05_latency_distribution_n20(tmp_path):
    cpp = _run_bench(CPP_EXE, runs=20, warmup=2)
    m2b = _run_bench(M2B_EXE, runs=20, warmup=2, cwd=str(tmp_path))
    speedup_p50 = cpp["p50_ms"] / m2b["p50_ms"]
    speedup_mean = cpp["mean_ms"] / m2b["mean_ms"]
    print(
        f"\n[BENCH 20x St(16,1024)] C++20: min={cpp['min_ms']:.2f}ms p50={cpp['p50_ms']:.2f}ms mean={cpp['mean_ms']:.2f}ms p95={cpp['p95_ms']:.2f}ms"
        f"\n[BENCH 20x St(16,1024)] M2B  : min={m2b['min_ms']:.2f}ms p50={m2b['p50_ms']:.2f}ms mean={m2b['mean_ms']:.2f}ms p95={m2b['p95_ms']:.2f}ms"
        f"\n[SPEEDUP]               p50={speedup_p50:.2f}x | mean={speedup_mean:.2f}x"
    )


def test_06_concurrent_execution_stress(tmp_path):
    def run_cpp(_):
        return subprocess.run([CPP_EXE], capture_output=True, text=True).returncode

    def run_m2b(idx):
        sub = tmp_path / f"w_{idx}"
        sub.mkdir(exist_ok=True)
        return subprocess.run([M2B_EXE], cwd=str(sub), capture_output=True, text=True).returncode

    with ThreadPoolExecutor(max_workers=8) as pool:
        cpp_codes = list(pool.map(run_cpp, range(8)))
        m2b_codes = list(pool.map(run_m2b, range(8)))

    assert cpp_codes == [0] * 8, f"Fallo concurrencia C++20: {cpp_codes}"
    assert m2b_codes == [0] * 8, f"Fallo concurrencia M2B: {m2b_codes}"


def test_07_zero_human_compiler_dependency():
    m2b_raw = _parse_pe64(M2B_EXE)["raw"].lower()
    for forbidden in (b"vcruntime", b"msvcp", b"api-ms-win-crt", b"ucrtbase"):
        assert forbidden not in m2b_raw, f"Dependencia CRT detectada: {forbidden}"
    assert b"kernel32.dll" in m2b_raw


def test_08_ghost_protocol_tuple_output(tmp_path):
    r_cpp = subprocess.run([CPP_EXE], capture_output=True, text=True)
    r_m2b = subprocess.run([M2B_EXE], cwd=str(tmp_path), capture_output=True, text=True)
    assert r_cpp.returncode == 0 and "ExitCode=0" in r_cpp.stdout and "SLAB_ID:" in r_cpp.stdout
    assert r_m2b.returncode == 0 and "ExitCode=0" in r_m2b.stdout and "SLAB_ID:" in r_m2b.stdout
    assert len(r_cpp.stdout) < 1024 and len(r_m2b.stdout) < 1024
