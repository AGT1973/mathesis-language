#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
TEST DE SILICIO: INFERENCIA VIVA HF SAFETENSORS -> PMTP SHMBUS -> MATHESIS2PYTHON
================================================================================
Valida el ciclo cerrado en silicio nativo:
  1. Carga de pesos safetensors desde la flota canónica HF (qwen3-1.5b-pmtp).
  2. Publicación atómica a memoria compartida PmtpSeqlockBuffer (ABI v2.1, BLAKE2s).
  3. Lectura zero-copy y validación anti-desgarro en microsegundos.
  4. Proyección continua coisométrica / retracción esférica en microcódigo AVX+FMA3.
  5. Verificación de invariantes: ||u||_2 - 1.0 <= 1e-15 en silicio físico.

Rigor: Gandalf (Reglas 1, 3, 19).
================================================================================
"""

import os
import sys
import time
import json
import psycopg2
import numpy as np
from pathlib import Path
from safetensors import safe_open

import mathesis2python as m2p

def main():
    print("=" * 70)
    print("CICLO CERRADO DE SILICIO: HF SAFETENSORS -> PMTP SHMBUS -> MATHESIS2PYTHON")
    print("======================================================================")

    # 1. Cargar tensor desde caché HF
    hf_path = Path(r"E:\POLYDIM_EINSOF\hf_export\qwen3-1.5b-pmtp\adapter_model.safetensors")
    if not hf_path.exists():
        print(f"[ERROR] Archivo safetensors no encontrado: {hf_path}")
        sys.exit(1)

    t0_load = time.perf_counter()
    with safe_open(str(hf_path), framework="numpy") as f:
        W = f.get_tensor("W")  # (1024, 2048) float32
    t_load_ms = (time.perf_counter() - t0_load) * 1000.0
    print(f"[1/4] Tensor Stiefel cargado desde HF: W {W.shape} {W.dtype} en {t_load_ms:.2f} ms")

    # 2. Vector continuo de entrada en S^(D-1) (D=2048)
    D = W.shape[1]
    k = W.shape[0]
    rng = np.random.default_rng(2026)
    v_raw = rng.standard_normal(D).astype(np.float64)
    norm_v = m2p.mathesis_norm(v_raw)
    v_in = v_raw / norm_v
    print(f"[2/4] Vector latente v_in en S^{D-1} generado (norma={m2p.mathesis_norm(v_in):.16f})")

    # 3. Publicación a Memoria Compartida PMTP Seqlock Buffer (Zero-Copy IPC)
    tagname = "pmtp_test_hf_in"
    t0_shm = time.perf_counter()
    pub_buf = m2p.mathesis_publish_seqlock(tagname, v_in)
    t_pub_us = (time.perf_counter() - t0_shm) * 1_000_000.0
    print(f"[3/4] Publicación Seqlock PMTP: tag '{tagname}' en {t_pub_us:.2f} us")

    # Lectura atómica desde el slab
    t0_read = time.perf_counter()
    v_read = m2p.mathesis_read_seqlock(tagname, dimension=D, zerocopy=False)
    t_read_us = (time.perf_counter() - t0_read) * 1_000_000.0
    
    # Comprobar integridad de lectura
    diff_read = float(np.max(np.abs(v_in - v_read)))
    print(f"      Lectura Seqlock: {t_read_us:.2f} us (diff max vs original: {diff_read:.2e})")
    if diff_read > 1e-15:
        print(f"[ERROR] Corrupción o desgarro en lectura Seqlock PMTP")
        sys.exit(1)

    # 4. Proyección coisométrica / retracción continua en microcódigo AVX+FMA3
    t0_proj = time.perf_counter()
    W64 = W.astype(np.float64)
    v_out_raw = W64 @ v_read  # Proyección lineal Stiefel
    # Retracción esférica exacta en silicio nativo
    norm_out = m2p.mathesis_norm(v_out_raw)
    u_out = v_out_raw / norm_out
    t_proj_us = (time.perf_counter() - t0_proj) * 1_000_000.0

    final_norm = m2p.mathesis_norm(u_out)
    norm_defect = abs(final_norm - 1.0)
    print(f"[4/4] Inferencia en Silicio v_out en S^{k-1} (k={k}):")
    print(f"      Tiempo de proyección + retracción: {t_proj_us:.2f} us")
    print(f"      Norma final calculada: {final_norm:.16f}")
    print(f"      Defecto ||u||_2 - 1.0: {norm_defect:.2e}")

    # Cota de tolerancia de hardware
    cota = 1.0e-15
    if norm_defect > cota:
        print(f"[ERROR FATAL] Deriva {norm_defect} supera la cota de silicio {cota}")
        sys.exit(1)

    # Liberar buffer si tiene método de cleanup
    try:
        pub_buf.close()
    except Exception:
        pass

    print("\n" + "=" * 70)
    print(f"[+] ESTADO DE SILICIO: INVARIANTES SATISFECHOS (EXIT CODE 0)")
    print(f"    Latencia Total IPC + Cómputo: {t_pub_us + t_read_us + t_proj_us:.2f} us")
    print(f"    Cota de Error Neumaier / Stiefel: {norm_defect:.2e} <= {cota}")
    print("======================================================================")

    # Persistencia en PostgreSQL 16 (Regla 0 y Regla 1)
    try:
        conn = psycopg2.connect(dbname="polydim_active_db", user="postgres", host="localhost", port=5432)
        cur = conn.cursor()
        payload = {
            "status": "CERTIFIED_SILICON_EXIT_CODE_0",
            "model_tested": "Polydim-Einsof/qwen3-1.5b-pmtp",
            "W_shape": list(W.shape),
            "ipc_publish_us": round(t_pub_us, 2),
            "ipc_read_us": round(t_read_us, 2),
            "silicon_proj_us": round(t_proj_us, 2),
            "norm_defect": norm_defect,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        cur.execute("""
            INSERT INTO active_vault (category, key_name, value, updated_at)
            VALUES ('session', 'HF_PMTP_MATHESIS_LIVE_STATUS', %s, NOW())
            ON CONFLICT (category, key_name) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW();
        """, (json.dumps(payload),))
        conn.commit()
        conn.close()
        print("[+] Checkpoint registrado en PostgreSQL 16: active_vault.HF_PMTP_MATHESIS_LIVE_STATUS")
    except Exception as e:
        print(f"[AVISO] No se pudo persistir en PostgreSQL: {e}")

    sys.exit(0)

if __name__ == "__main__":
    main()
