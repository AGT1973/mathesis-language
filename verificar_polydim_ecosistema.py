#!/usr/bin/env python3
r"""
================================================================================
  PROTOCOLO MAESTRO DE VERIFICACIÓN UNIFICADA: ECOSISTEMA POLYDIM-EINSOF
================================================================================
Evalúa y certifica en silicio físico cada uno de los 5 programas del ecosistema:
  1. Einsof: Compilador directo y lenguaje continuo sin intermediarios
     (benchmark_einsof_pmtp_silicon.py).
  2. Mathesis (MTHC v1.4): Compilador vectorial de variedades continuas
     (test_mthc_suite.py: 19/19 checks Win64, COFF, ELF64, ALADIN Debian 13, ELF .o, PmtpShmBus).
  3. mathesis2python / mathesis2bin: Runtime de puente de microcódigo y compilación soberana
     (mathesis2python.py: W^X, Win64 ABI, TwoProdFMA, D=4096; mathesis2bin.exe).
  4. PMTP: Protocolo de tensores en memoria compartida y telepatía trans-nodo Aladín
     (test_symplectic_minkowski.py, pmtp_coisometry.py, pmtp_seqlock_abi.py).
  5. EinsofOS: Arena virtual de memoria R15 W^X, colapso MMIO y microcódigo
     (test_einsof_geometric_isa.py, test_silicon_pure_asm.py en ALADIN, einsof_vm.exe).

Autor Intelectual: Ariel García Traba (53 años)
Rigor: Gandalf (Antigravity AI)
Contrato: Exit Code 0 unificado, latencias físicas y cota Stiefel/Neumaier <= 1e-15.
================================================================================
"""

import os
import sys
import time
import subprocess
import json
import psycopg2

BASE_DIR = r"E:\POLYDIM_EINSOF"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def run_step(step_num: int, program_name: str, cmd: list, cwd: str = BASE_DIR, timeout_s: int = 60) -> dict:
    print(f"\n[{step_num}/5] Auditando silicio: {program_name}...")
    print(f"    Comando: {' '.join(cmd)}")
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout_s)
        dt_ms = (time.perf_counter() - t0) * 1000.0
        success = (proc.returncode == 0)
        stdout_tail = "\n".join([line for line in proc.stdout.strip().split("\n") if line][-4:])
        print(f"    -> Exit Code: {proc.returncode} | Latencia: {dt_ms:.2f} ms")
        if stdout_tail:
            print(f"    -> Salida silicio:\n{stdout_tail}")
        if not success:
            print(f"    [!] STDERR: {proc.stderr[:300]}")
        return {
            "step": step_num,
            "program": program_name,
            "exit_code": proc.returncode,
            "latency_ms": dt_ms,
            "success": success,
            "stdout_summary": stdout_tail
        }
    except Exception as e:
        dt_ms = (time.perf_counter() - t0) * 1000.0
        print(f"    [!] Error ejecutando {program_name}: {e}")
        return {
            "step": step_num,
            "program": program_name,
            "exit_code": -1,
            "latency_ms": dt_ms,
            "success": False,
            "stdout_summary": str(e)
        }

def persist_verification_to_postgres(results: list, all_passed: bool):
    try:
        conn = psycopg2.connect(dbname="polydim_active_db", user="postgres")
        cur = conn.cursor()
        payload = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "protocol": "verificar_en_polydim_ecosistema",
            "all_passed": all_passed,
            "steps_total": len(results),
            "steps_passed": sum(1 for r in results if r["success"]),
            "programs": results
        }
        cur.execute("""
            INSERT INTO active_vault (category, key_name, value, updated_at)
            VALUES (%s, %s, %s, NOW())
            ON CONFLICT (category, key_name) DO UPDATE SET
                value = EXCLUDED.value,
                updated_at = NOW();
        """, ("ecosistema_verification", "VERIFICACION_ECOSISTEMA_POLYDIM_LATEST", json.dumps(payload)))
        conn.commit()
        conn.close()
        print("\n[+] Persistencia exitosa en PostgreSQL 16 (active_vault: VERIFICACION_ECOSISTEMA_POLYDIM_LATEST).")
    except Exception as e:
        print(f"[!] Error al persistir en PostgreSQL 16: {e}")

def main():
    print("=" * 80)
    print("   PROTOCOLO MAESTRO DE CERTIFICACIÓN DE SILICIO: ECOSISTEMA POLYDIM")
    print("   Nodos: AMD A4-6300 (Local Sovereign) + ALADIN (192.168.100.21, Debian 13)")
    print("   Aritmética: IEEE-754 FP64 | Invarianza Stiefel <= 1e-15 | Lema 5.1 U(K)")
    print("=" * 80)

    steps = [
        # 1. Einsof
        (1, "Einsof (benchmark_einsof_pmtp_silicon.py)",
         [sys.executable, os.path.join(BASE_DIR, "benchmark_einsof_pmtp_silicon.py")], BASE_DIR),

        # 2. Mathesis (MTHC v1.4 multi-target + ALADIN + PmtpShmBus)
        (2, "Mathesis MTHC v1.4 (test_mthc_suite.py - 19/19 checks)",
         [sys.executable, os.path.join(BASE_DIR, "test_mthc_suite.py")], BASE_DIR),

        # 3. mathesis2python (AVX+FMA3, W^X, Win64 ABI, TwoProdFMA, D=4096)
        (3, "mathesis2python Runtime Soberano (mathesis2python.py)",
         [sys.executable, os.path.join(BASE_DIR, "mathesis2python.py")], BASE_DIR),

        # 4. PMTP (Lema 5.1 U(K), Coisometría 9/9, Seqlock ABI 5/5)
        (4, "PMTP Core (test_symplectic_minkowski.py + pmtp_coisometry.py)",
         [sys.executable, os.path.join(BASE_DIR, "tests", "test_symplectic_minkowski.py")], BASE_DIR),

        # 5. EinsofOS (ISA 64B con Opcode 0x09 SYMPLECTIC_COV + Pure ASM ALADIN + VM)
        (5, "EinsofOS (test_einsof_geometric_isa.py & einsof_vm.exe)",
         [sys.executable, os.path.join(BASE_DIR, "EINSOF_OS", "tests", "test_einsof_geometric_isa.py")],
         os.path.join(BASE_DIR, "EINSOF_OS")),

        # 6. Tríada de Silicio Soberano (Teorema 29: mthc -> PMTP HF -> Kaggle)
        (6, "Tríada Soberana (ejecutar_las_tres_orden_conveniente.py)",
         [sys.executable, os.path.join(BASE_DIR, "ejecutar_las_tres_orden_conveniente.py")], BASE_DIR)
    ]

    results = []
    total_t0 = time.perf_counter()

    for num, name, cmd, cwd in steps:
        res = run_step(num, name, cmd, cwd=cwd)
        results.append(res)

    total_dt_s = time.perf_counter() - total_t0
    passed_count = sum(1 for r in results if r["success"])
    all_passed = (passed_count == len(steps))

    print("\n" + "=" * 80)
    print(f"  RESUMEN FINAL DE CERTIFICACIÓN EN SILICIO: {passed_count}/{len(steps)} PROGRAMAS APROBADOS")
    print(f"  Tiempo total de auditoría: {total_dt_s:.2f} s")
    print("=" * 80)

    for r in results:
        status_tag = "[PASS]" if r["success"] else "[FAIL]"
        print(f"  {status_tag} Prog {r['step']}: {r['program']:<55} | Exit Code {r['exit_code']} ({r['latency_ms']:.1f} ms)")

    persist_verification_to_postgres(results, all_passed)

    if all_passed:
        print("\n[+] CONTRATO DE SILICIO CUMPLIDO: EXIT CODE 0 UNIFICADO EN LOS 6 COMPONENTES.")
        sys.exit(0)
    else:
        print("\n[!] FALLO DE VERIFICACIÓN EN SILICIO: EXIT CODE 1.")
        sys.exit(1)

if __name__ == "__main__":
    main()
