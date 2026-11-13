#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ORQUESTADOR MAESTRO: LAS TRES RAMAS EN EL ORDEN MÁS CONVENIENTE
================================================================================
Orden Lógico de Dependencia y Cómputo:
  FASE 1: Fundamento de Silicio — Compilación y Hardware Gate (mthc.py v1.4+)
          -> Cero dependencias C, PE32+ Win64 y ELF64 nativo, Exit Code 0.
  FASE 2: Enlace Vivo de Inferencia — HF Safetensors -> PMTP ShmBus -> mathesis2python
          -> Lectura Seqlock microsegundo, sin texto 1D, deriva Stiefel <= 1e-15.
  FASE 3: Expansión de Flota — Pipeline de Fine-Tuning Stiefel Kaggle/Colab
          -> Exportación dual (safetensors + bin), notebook para cuota free 30h.

Rigor: Gandalf (Reglas 1, 2, 3, 14, 19).
================================================================================
"""

import os
import sys
import time
import subprocess
import json
import psycopg2
from pathlib import Path

BASE_DIR = Path(r"E:\POLYDIM_EINSOF")

def log_header(title: str):
    print("\n" + "=" * 75)
    print(f"  {title}")
    print("=" * 75)

def run_phase(phase_num: int, name: str, cmd: list, cwd: Path = BASE_DIR) -> dict:
    log_header(f"FASE {phase_num}: {name}")
    print(f"[*] Ejecutando: {' '.join(cmd)}")
    t0 = time.perf_counter()
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    dt_ms = (time.perf_counter() - t0) * 1000.0
    
    print(f"[*] Latencia: {dt_ms:.2f} ms | Exit Code: {proc.returncode}")
    if proc.stdout:
        # Imprimir resumen de salida limpia
        lines = [l for l in proc.stdout.splitlines() if l.strip()]
        for l in lines[-6:]:
            print(f"    {l}")
            
    if proc.returncode != 0:
        print(f"[!] STDERR: {proc.stderr[:400]}")
        return {"phase": phase_num, "name": name, "success": False, "exit_code": proc.returncode, "latency_ms": dt_ms}
        
    return {"phase": phase_num, "name": name, "success": True, "exit_code": 0, "latency_ms": dt_ms}

def main():
    t_global_0 = time.perf_counter()
    print("=" * 75)
    print("   POLYDIM-EINSOF: EJECUCIÓN INTEGRADA EN ORDEN CONVENIENTE")
    print("   (1. Silicio Soberano -> 2. Inferencia PMTP Viva -> 3. Fine-Tuning Kaggle)")
    print("=" * 75)

    results = []

    # ──────────────────────────────────────────────────────────────────────────
    # FASE 1: Silicio Soberano y Compilador Mathesis (mthc.py)
    # ──────────────────────────────────────────────────────────────────────────
    # 1.1 Compilar test_collapse_1d_mmio.mth a ejecutable Win64 nativo
    res_compile = run_phase(
        1, "Compilación PE32+ Nativa (mthc.py)",
        [sys.executable, "mthc.py", "test_collapse_1d_mmio.mth", "-o", "test_collapse_1d_mmio.exe"]
    )
    results.append(res_compile)
    if not res_compile["success"]:
        sys.exit(1)

    # 1.2 Ejecutar el binario generado directamente en silicio físico
    res_exec = run_phase(
        1, "Ejecución en Silicio de test_collapse_1d_mmio.exe",
        [str(BASE_DIR / "test_collapse_1d_mmio.exe")]
    )
    results.append(res_exec)
    if not res_exec["success"]:
        sys.exit(1)

    # ──────────────────────────────────────────────────────────────────────────
    # FASE 2: Inferencia Viva HF Safetensors -> PMTP ShmBus -> mathesis2python
    # ──────────────────────────────────────────────────────────────────────────
    res_pmtp = run_phase(
        2, "Puente Cerrado: HF Safetensors -> PMTP Seqlock -> mathesis2python",
        [sys.executable, "test_live_hf_to_pmtp_mathesis.py"]
    )
    results.append(res_pmtp)
    if not res_pmtp["success"]:
        sys.exit(1)

    # ──────────────────────────────────────────────────────────────────────────
    # FASE 3: Expansión de Flota y Pipeline Stiefel Kaggle / Colab
    # ──────────────────────────────────────────────────────────────────────────
    res_kaggle = run_phase(
        3, "Pipeline Stiefel Kaggle/Colab (Test Silicio + Export Dual + Notebook)",
        [sys.executable, "einsof_kaggle_stiefel_pipeline.py", "--test-silicon"]
    )
    results.append(res_kaggle)
    if not res_kaggle["success"]:
        sys.exit(1)

    # ──────────────────────────────────────────────────────────────────────────
    # CIERRE Y PERSISTENCIA ATÓMICA EN POSTGRESQL 16
    # ──────────────────────────────────────────────────────────────────────────
    t_global_total = (time.perf_counter() - t_global_0) * 1000.0
    all_ok = all(r["success"] for r in results)

    print("\n" + "=" * 75)
    print("   RESUMEN FINAL DE CERTIFICACIÓN UNIFICADA")
    print(f"   Estado Global: {'CERTIFICADO EXIT CODE 0' if all_ok else 'FALLO'}")
    print(f"   Tiempo Total de Ejecución: {t_global_total:.2f} ms")
    for r in results:
        status_tag = "PASS (EC=0)" if r["success"] else f"FAIL (EC={r['exit_code']})"
        print(f"   - Fase {r['phase']} [{r['name']}]: {status_tag} en {r['latency_ms']:.2f} ms")
    print("=" * 75)

    try:
        conn = psycopg2.connect(dbname="polydim_active_db", user="postgres", host="localhost", port=5432)
        cur = conn.cursor()
        vault_payload = {
            "status": "UNIFIED_PIPELINE_CONVENIENT_ORDER_SUCCESS",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_latency_ms": round(t_global_total, 2),
            "phases": results,
            "rule_enforced": "Reglas 1, 2, 3, 14, 19 (Silicio Soberano, Cero Costo, PMTP ShmBus)"
        }
        cur.execute("""
            INSERT INTO active_vault (category, key_name, value, updated_at)
            VALUES ('session', 'MASTER_THREE_PILLARS_CONVENIENT_ORDER', %s, NOW())
            ON CONFLICT (category, key_name) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW();
        """, (json.dumps(vault_payload),))
        conn.commit()
        conn.close()
        print("[+] Persistencia en active_vault: MASTER_THREE_PILLARS_CONVENIENT_ORDER registrada.")
    except Exception as e:
        print(f"[!] Error al persistir en PostgreSQL 16: {e}")

    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
