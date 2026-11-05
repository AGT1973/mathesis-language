#!/usr/bin/env python3
"""
MATHESIS SILICON DISASSEMBLER & INSPECTOR (V1.0)
Inspecciona tuplas binarias de 64 bytes de MATHESIS y muestra su semántica geométrica.
"""

import struct
import sys
import os

OPCODE_NAMES = {
    0x01: "ROT_LIE_SO",
    0x02: "RETRACT_STIEFEL",
    0x03: "PROJECT_GRASSMANN",
    0x04: "CLIFFORD_MULT",
    0x05: "DIALECTIC_LYAPUNOV",
    0x06: "PMTP_TELEPATHY",
    0x07: "COLLAPSE_MMIO",
    0x08: "HALT_EQUILIBRIUM"
}

STRUCT_FMT = "<BBHI III f ddd Q II"

def disassemble(file_path: str):
    if not os.path.exists(file_path):
        print(f"[-] Archivo no encontrado: {file_path}")
        return

    size = os.path.getsize(file_path)
    if size % 64 != 0 or size == 0:
        print(f"[-] Tamano invalido: {size} bytes (debe ser multiplo de 64)")
        return

    num_ops = size // 64
    print("=" * 75)
    print(f"  DESENSAMBLADOR SILICIO MATHESIS: {file_path}")
    print(f"  Total tuplas: {num_ops} | Tamano total: {size} bytes (64B/cache-line)")
    print("=" * 75)
    print(f"{'IP':<4} | {'OPCODE':<20} | {'DIM':<6} | {'SLAB SRC':<10} | {'SLAB DEST':<10} | {'DETALLES'}")
    print("-" * 75)

    with open(file_path, "rb") as f:
        for ip in range(num_ops):
            raw = f.read(64)
            unpacked = struct.unpack(STRUCT_FMT, raw)
            opcode, flags, dim, sage_mask, src_a, src_b, dest, dt, theta, alpha, gamma, neumaier, core, pad = unpacked

            op_name = OPCODE_NAMES.get(opcode, f"UNKNOWN(0x{opcode:02X})")
            src_str = f"0x{src_a:X},0x{src_b:X}" if src_b else f"0x{src_a:X}"
            dest_str = f"0x{dest:X}"

            details = []
            if opcode == 0x01:
                details.append(f"theta={theta:.4f}")
            elif opcode == 0x05:
                details.append(f"sages=0x{sage_mask:02X} alpha={alpha:.2f} gamma={gamma:.2f}")
            elif opcode == 0x07:
                details.append("GOP 60Hz O(1) Purge")

            print(f"{ip:03d}  | {op_name:<20} | {dim:<6} | {src_str:<10} | {dest_str:<10} | {' '.join(details)}")

    print("=" * 75)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "E:\\MATHESIS\\examples\\dialogo_sabios_euler_gauss.mat"
    disassemble(path)
