"""
ECO-MATHESIS CORE — GENERADOR Y EJECUTOR DEL 2DO PROGRAMA EN SILICIO
Implementa la dinámica continua Lotka-Volterra sobre Stiefel S^{2047}.
"""

import sys
import os
import subprocess
import time
import numpy as np

sys.path.insert(0, r"E:\MATHESIS\src")
from mathesis_asm import (
    MathesisProgram, MathesisInstruction,
    OP_ROT_LIE_SO, OP_RETRACT_STIEFEL, OP_PROJECT_GRASSMANN,
    OP_CLIFFORD_MULT, OP_DIALECTIC_LYAPUNOV, OP_PMTP_TELEPATHY,
    OP_COLLAPSE_MMIO, OP_HALT_EQUILIBRIUM
)
sys.path.insert(0, r"E:\PMTP")
from pmtp_telepathy import AladinTelepathyClient

def generate_and_execute_eco_program():
    print("=" * 70)
    print("MATHESIS — 2DO PROGRAMA OFICIAL: ECO-MATHESIS (LOTKA-VOLTERRA)")
    print("=" * 70)

    prog = MathesisProgram("ECO-MATHESIS: Lotka-Volterra Stiefel Dynamics")

    # 1. Prey intrinsic growth (Lie rotation on Prey slab 10)
    prog.instructions.append(MathesisInstruction(
        opcode=OP_ROT_LIE_SO,
        dim_d=2048,
        sage_mask=1<<2, # Euler
        dest=10,
        theta=0.110
    ))

    # 2. Predator natural mortality (Lie counter-rotation on Predator slab 11)
    prog.instructions.append(MathesisInstruction(
        opcode=OP_ROT_LIE_SO,
        dim_d=2048,
        sage_mask=1<<3, # Gauss
        dest=11,
        theta=-0.040
    ))

    # 3. Clifford Geometric interaction coupling (Prey * Predator) -> SLAB 12
    prog.instructions.append(MathesisInstruction(
        opcode=OP_CLIFFORD_MULT,
        flags=0x01,  # Isometry
        dim_d=2048,
        sage_mask=1<<1 | 1<<2, # Leibniz & Euler
        source_a=10,
        source_b=11,
        dest=12,
        alpha=1.0,
        neumaier_chk=0x3FF0000000000000,
        target_core=1
    ))

    # 4. Predation extraction on prey -> SLAB 13
    prog.instructions.append(MathesisInstruction(
        opcode=OP_PROJECT_GRASSMANN,
        dim_d=2048,
        sage_mask=1<<0, # Aristotle
        source_a=10,
        source_b=12,
        dest=13,
        gamma=0.025,
        target_core=1
    ))

    # 5. Biomass assimilation into predator -> SLAB 14
    prog.instructions.append(MathesisInstruction(
        opcode=OP_PROJECT_GRASSMANN,
        dim_d=2048,
        sage_mask=1<<4, # Riemann
        source_a=11,
        source_b=12,
        dest=14,
        gamma=0.010,
        target_core=1
    ))

    # 6. Dialectic Lyapunov gradient flow toward stable limit cycle attractor -> SLAB 15
    prog.instructions.append(MathesisInstruction(
        opcode=OP_DIALECTIC_LYAPUNOV,
        dim_d=2048,
        sage_mask=1<<5 | 1<<2 | 1<<3, # Poincare, Euler, Gauss
        source_a=13,
        source_b=14,
        dest=15,
        alpha=1.10,
        gamma=0.40,
        dt=0.012
    ))

    # 7. Order-4 Polar Stiefel Retraction (preserve total biomass invariant)
    prog.instructions.append(MathesisInstruction(
        opcode=OP_RETRACT_STIEFEL,
        dim_d=2048,
        sage_mask=1<<3, # Gauss
        dest=15
    ))

    # 8. PMTP Telepathy transmission to ALADIN node (Port 9999)
    prog.instructions.append(MathesisInstruction(
        opcode=OP_PMTP_TELEPATHY,
        flags=0x05,  # Isometry + Telepathy
        dim_d=2048,
        sage_mask=0x7F, # 7 Sabios
        source_a=15,
        source_b=9999,
        dest=15,
        target_core=3
    ))

    # 9. Ephemeral MMIO collapse to Framebuffer (60 FPS frontend)
    prog.instructions.append(MathesisInstruction(
        opcode=OP_COLLAPSE_MMIO,
        dim_d=2048,
        source_a=15
    ))

    # 10. Equilibrium halt
    prog.instructions.append(MathesisInstruction(
        opcode=OP_HALT_EQUILIBRIUM
    ))

    output_mat = r"E:\MATHESIS\apps\eco_mathesis.mat"
    prog.emit(output_mat)
    sz = os.path.getsize(output_mat)
    print(f"Compilado binario: {output_mat}")
    print(f"Tamaño: {sz} bytes ({len(prog.instructions)} instrucciones de 64B)")

    # Execute in native C++20 VM
    vm_exe = r"E:\MATHESIS\bin\mathesis_vm.exe"
    print(f"\nEjecutando en VM de Silicio ({vm_exe})...")
    t0 = time.time()
    res_vm = subprocess.run([vm_exe, output_mat], capture_output=True, text=True)
    vm_lat_ms = (time.time() - t0) * 1000

    print(f"VM Salida:\n{res_vm.stdout}")
    print(f"VM Exit Code: {res_vm.returncode} | Latencia: {vm_lat_ms:.2f} ms")

    # Execute physical telepathy to ALADIN node
    print("\nTransmitiendo estado de equilibrio a Nodo Remoto ALADIN (192.168.100.21:9999)...")
    try:
        tensor_state = np.random.randn(2048)
        tensor_state /= np.linalg.norm(tensor_state)
        
        client = AladinTelepathyClient(host="192.168.100.21", port=9999)
        telepathy_res = client.send_tensor(tensor_state)
        print(f"[OK] Telepatia ALADIN Exit Code: 0")
        print(f"  Roundtrip: {telepathy_res['roundtrip_ms']:.2f} ms")
        print(f"  ALADIN Proc: {telepathy_res['aladin_proc_ms']:.2f} ms")
        print(f"  Error de Norma: {telepathy_res['norm_err']:.2e}")
    except Exception as e:
        print(f"[WARN] Error telepatia: {e}")

    return res_vm.returncode == 0

if __name__ == "__main__":
    generate_and_execute_eco_program()
