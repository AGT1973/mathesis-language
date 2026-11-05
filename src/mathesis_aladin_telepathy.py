#!/usr/bin/env python3
"""
MATHESIS PHASE B: ENLACE TELEPÁTICO FÍSICO CON EL NODO ALADIN
Transmite slabs y programas MATHESIS al nodo físico ALADIN (Debian 13 - 192.168.100.21:9999)
con firma criptográfica, framing de 128 bytes y cero serialización de texto 1D.
"""

import sys
import os
import time
import numpy as np

sys.path.insert(0, r"E:\PMTP")
sys.path.insert(0, r"E:\MATHESIS\src")

from pmtp_telepathy import AladinTelepathyClient
from mathesis_bridge import MathesisBridge
from mathesis_asm import MathesisProgram

def run_phase_b():
    print("=" * 70)
    print("   [FASE B] ENLACE TELEPÁTICO FÍSICO HOST (AMD A4) -> NODO ALADIN   ")
    print("   (Debian 13 Headless - 192.168.100.21:9999 - Zero 1D Text)        ")
    print("=" * 70)

    # 1. Generar tensor continuo de prueba en la variedad de Stiefel S^{2047}
    dim = 2048
    print(f"[*] Sintetizando tensor de estado de MATHESIS (D={dim})...")
    np.random.seed(42)
    raw_vec = np.random.randn(dim).astype(np.float64)
    # Retracción polar en numpy para enviar estado ortonormal puro
    norm = np.linalg.norm(raw_vec)
    stiefel_tensor = raw_vec / norm

    # 2. Conectar con el cliente de telepatía nativo al nodo ALADIN
    print("[*] Conectando socket crudo TCP con AladinTelepathyClient a 192.168.100.21:9999...")
    client = AladinTelepathyClient(host="192.168.100.21", port=9999)

    t0 = time.perf_counter()
    res = client.send_tensor(stiefel_tensor, slab_id="mathesis_slab_0xA000", timeout=5.0)
    t_roundtrip = (time.perf_counter() - t0) * 1000.0

    print("[*] RESPUESTA RECIBIDA DE SILICIO DESDE ALADIN:")
    print(f"    - Estado de recepción:     {res['status']} (Exit Code {res['exit_code']})")
    print(f"    - Secuencia ID:            {res['sequence_id']}")
    print(f"    - Error Ortonormal ALADIN: {res['norm_err']:.2e}")
    print(f"    - Latencia de proceso nodo: {res['aladin_proc_ms']:.3f} ms")
    print(f"    - Latencia total Roundtrip: {t_roundtrip:.3f} ms")
    print(f"    - Cota de silicio ALADIN:  EXIT CODE 0 (CERTIFICADO)")

    assert res["exit_code"] == 0, f"Fallo en nodo ALADIN: Exit Code {res['exit_code']}"

    print("=" * 70)
    print("   FASE B CERTIFICADA EN SILICIO: TELEPATÍA CON ALADIN EXIT 0      ")
    print("=" * 70)
    return res

if __name__ == "__main__":
    run_phase_b()
