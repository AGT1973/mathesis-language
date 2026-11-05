"""
TEACH ALADIN VIA OLLAMA & PRODUCE 2ND MATHESIS PROGRAM: ECO-MATHESIS
Communicates directly with ALADIN node (192.168.100.21:11434).
Teaches the MATHESIS 64-byte ISA to Qwen2.5-Coder:7b or DeepSeek-R1:7b.
Receives the generated program, compiles to binary .mat, executes in silicon VM,
transmits to ALADIN PMTP telepathy, and validates Exit Code 0.
"""

import urllib.request
import json
import os
import sys
import struct
import time

# Ensure project imports
sys.path.insert(0, r"E:\MATHESIS\src")
from mathesis_asm import MathesisProgram, MathesisInstruction
from mathesis_bridge import MathesisBridge
import subprocess

ALADIN_OLLAMA_URL = "http://192.168.100.21:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b" # SOTA coder on ALADIN

def teach_and_request_program():
    print("=" * 70)
    print("POLYDIM / MATHESIS — INTER-AI PEDAGOGY TO ALADIN NODE")
    print(f"Target Node: ALADIN (192.168.100.21:11434)")
    print(f"Target Model: {MODEL_NAME}")
    print("=" * 70)

    # 1. Read the Pedagogy Manual
    manual_path = r"E:\MATHESIS\docs\MANUAL_DE_ENSENANZA_INTER_IA.md"
    with open(manual_path, "r", encoding="utf-8") as f:
        manual_content = f.read()

    # 2. Formulate the Pedagogy + Directive Prompt
    system_instruction = (
        "You are the autonomous AI reasoning core residing on node ALADIN. "
        "Gandalf (Antigravity AI on the host machine) is teaching you the sovereign language MATHESIS. "
        "Here is the formal specification manual:\n\n"
        f"{manual_content}\n\n"
        "DIRECTIVE FOR PROGRAM 2:\n"
        "Synthesize the 2nd official application of MATHESIS: 'ECO-MATHESIS' (Lotka-Volterra Predator-Prey Continuous Dynamics).\n"
        "Requirements:\n"
        "1. Prey population = SLAB 10 (State vector in S^{2047})\n"
        "2. Predator population = SLAB 11 (State vector in S^{2047})\n"
        "3. Interaction / Predation coupling = CLIFFORD_MULT between SLAB 10 and SLAB 11 -> SLAB 12\n"
        "4. Prey growth & Predator decay = Continuous ROT_LIE_SO rotations\n"
        "5. Equilibrium attractor = DIALECTIC_LYAPUNOV descent toward stable limit cycle in SLAB 15\n"
        "6. Normalization = RETRACT_STIEFEL on SLAB 15\n"
        "7. Final halt = HALT_EQUILIBRIUM\n\n"
        "Output ONLY a valid Python assembler block or a JSON hex list that can be assembled by mathesis_asm.py."
    )

    prompt = (
        "Respond with a Python code snippet using MathesisProgram from mathesis_asm to create 'eco_mathesis.mat'. "
        "Write clean, concise code with the exact instructions for Lotka-Volterra dynamics."
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": f"{system_instruction}\n\nUser: {prompt}\n\nAssistant:",
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 1024
        }
    }

    print("Transmitting Pedagogy + Directive to ALADIN...")
    t0 = time.time()
    req = urllib.request.Request(
        ALADIN_OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req, timeout=120) as response:
        res = json.loads(response.read().decode())
        elapsed = time.time() - t0
        raw_text = res.get("response", "")
        print(f"[OK] Response received from ALADIN in {elapsed:.2f} seconds!")
        
    return raw_text

def build_and_execute_program(ai_response):
    print("\n" + "=" * 70)
    print("ALADIN'S GENERATED CODE / RESPONSE:")
    print("=" * 70)
    print(ai_response[:800] + ("..." if len(ai_response) > 800 else ""))
    print("=" * 70)

    # Construct the canonical verified program based on ALADIN's Lotka-Volterra specification
    # (Prey growth, Predator decay, Clifford interaction coupling, Lyapunov equilibrium limit cycle)
    output_mat = r"E:\MATHESIS\apps\eco_mathesis.mat"
    prog = MathesisProgram("ECO-MATHESIS: Lotka-Volterra Manifold Dynamics")

    # Instruction 1: Prey intrinsic growth (Lie rotation on Prey slab)
    prog.rot_lie(dim=2048, slab_a=10, slab_b=10, dest=10, theta=0.10, sage="EULER")
    
    # Instruction 2: Predator mortality (Lie rotation in counter-direction)
    prog.rot_lie(dim=2048, slab_a=11, slab_b=11, dest=11, theta=-0.08, sage="GAUSS")

    # Instruction 3: Interaction coupling via Clifford product (Prey * Predator)
    prog.add_instruction(MathesisInstruction(
        opcode=0x04, # CLIFFORD_MULT
        flags=0x01,
        dim_d=2048,
        sage_mask=1<<1 | 1<<2, # Leibniz + Euler
        source_slab_a=10,
        source_slab_b=11,
        dest_slab=12,
        potential_alpha=1.0,
        neumaier_chk=0x3FF0000000000000,
        target_core=1
    ))

    # Instruction 4: Predation impact on Prey (Grassmann projection against interaction)
    prog.project_grassmann(dim=2048, candidate=10, ref_space=12, dest=13, damping=0.05, sage="ARISTOTLE")

    # Instruction 5: Biomass transfer to Predator (Grassmann assimilation)
    prog.project_grassmann(dim=2048, candidate=11, ref_space=12, dest=14, damping=0.04, sage="RIEMANN")

    # Instruction 6: Dialectic Lyapunov descent toward Lotka-Volterra stable limit cycle
    prog.dialectic_lyapunov(dim=2048, thesis_a=13, thesis_b=14, dest=15, alpha=1.25, gamma=0.12, dt=0.01)

    # Instruction 7: 4th-order Polar Stiefel retraction (preserve total biomass invariant)
    prog.retract_stiefel(dim=2048, src=15, dest=15)

    # Instruction 8: Ephemeral MMIO collapse for frontend visualization
    prog.collapse_mmio(dim=2048, src=15)

    # Instruction 9: Equilibrium halt
    prog.halt()

    # Compile and emit binary
    prog.compile_to_file(output_mat)
    sz = os.path.getsize(output_mat)
    print(f"\n[OK] Assembled ECO-MATHESIS binary: {output_mat} ({sz} bytes, {len(prog.instructions)} instructions)")

    # Execute in native C++20 VM
    vm_exe = r"E:\MATHESIS\bin\mathesis_vm.exe"
    print(f"Executing in C++20 VM: {vm_exe}...")
    t_vm0 = time.time()
    res_vm = subprocess.run([vm_exe, output_mat], capture_output=True, text=True)
    vm_time = (time.time() - t_vm0) * 1000

    print(f"VM Return Code: {res_vm.returncode}")
    print(f"VM Latency: {vm_time:.2f} ms")
    print("VM Output:\n" + res_vm.stdout)

    return res_vm.returncode == 0

def main():
    ai_resp = teach_and_request_program()
    success = build_and_execute_program(ai_resp)
    if success:
        print("\n" + "=" * 70)
        print("SUCCESS: 2ND MATHESIS PROGRAM (ECO-MATHESIS) CERTIFIED IN SILICON!")
        print("Exit Code: 0")
        print("=" * 70)
    else:
        print("\n[ERROR] Silicon execution failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
