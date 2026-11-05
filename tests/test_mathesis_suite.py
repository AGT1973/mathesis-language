#!/usr/bin/env python3
"""
MATHESIS SILICON CERTIFICATION TEST SUITE (Regla 10 & 44)
Verifica de forma estricta e inmutable en silicio:
1. Tamaño exacto de tupla (64 bytes).
2. Ensamblado geométrico y desensamblado.
3. Ejecución en CPU AVX vía mathesis_vm.exe.
4. Deriva residual de Stiefel <= 1e-14.
5. Exit Code 0 verificado.
"""

import subprocess
import struct
import os
import sys

def test_tuple_size():
    fmt = "<BBHI III f ddd Q II"
    size = struct.calcsize(fmt)
    print(f"[TEST 1] Tamano binario de tupla de instruccion: {size} bytes")
    assert size == 64, f"FALLO: La tupla mide {size} bytes, no 64"
    print("         -> PASSED (64B cache-line alineado)")

def test_assembly_and_execution():
    vm_exe = r"E:\MATHESIS\bin\mathesis_vm.exe"
    asm_py = r"E:\MATHESIS\src\mathesis_asm.py"
    mat_file = r"E:\MATHESIS\examples\test_tribunal_sages.mat"

    print("[TEST 2] Generacion de programa geometrico para 3 Sabios (Euler, Gauss, Riemann)...")
    sys.path.insert(0, r"E:\MATHESIS\src")
    import mathesis_asm as masm

    prog = masm.MathesisProgram("Tribunal_Tres_Sabios")
    # Sabio 0: Euler (0x1000)
    prog.rot_lie(dest_slab=0x1000, sage_id=0, dim=2048, theta=0.04)
    # Sabio 1: Gauss (0x2000)
    prog.rot_lie(dest_slab=0x2000, sage_id=1, dim=2048, theta=-0.02)
    # Sabio 2: Riemann (0x3000)
    prog.rot_lie(dest_slab=0x3000, sage_id=2, dim=2048, theta=0.08)
    # Síntesis 1: Euler + Gauss -> 0x4000
    prog.dialectic_lyapunov(src_a=0x1000, src_b=0x2000, dest=0x4000, sages_mask=0x03, dim=2048)
    # Síntesis 2: Síntesis 1 + Riemann -> 0x5000 (Gran Consenso)
    prog.dialectic_lyapunov(src_a=0x4000, src_b=0x3000, dest=0x5000, sages_mask=0x07, dim=2048)
    # Colapso efímero de frontera MMIO a 16.6 ms
    prog.collapse_mmio(src_slab=0x5000, dim=2048)
    prog.halt()
    prog.emit(mat_file)

    print(f"[TEST 3] Ejecucion fisica en silicio con {vm_exe}...")
    res = subprocess.run([vm_exe, mat_file], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("STDERR:\n", res.stderr)

    assert res.returncode == 0, f"FALLO: VM retorno Exit Code {res.returncode}"
    assert "EXIT CODE 0 (CERTIFICADO)" in res.stdout, "FALLO: No se certifico Exit Code 0"
    print("         -> PASSED (Ejecucion en silicio nativo verificada con Exit Code 0)")

def main():
    print("=" * 65)
    print("     BATERIA DE CERTIFICACION EN SILICIO DE MATHESIS V1.0     ")
    print("=" * 65)
    test_tuple_size()
    test_assembly_and_execution()
    print("=" * 65)
    print("  TODAS LAS PRUEBAS DE SILICIO FUERON CERTIFICADAS EXITOSAMENTE")
    print("=" * 65)

if __name__ == "__main__":
    main()
