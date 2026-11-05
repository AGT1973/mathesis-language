#!/usr/bin/env python3
"""
MATHESIS INTER-AI BRIDGE & TRANSFER ENGINE (V1.0)
Permite a cualquier modelo de IA empaquetar, transferir, recibir y ejecutar
programas MATHESIS de 64 bytes a través de memoria compartida o canales de texto 1D.
"""

import base64
import hashlib
import struct
import os
import sys
import subprocess

HEADER_TAG = "---BEGIN MATHESIS TUPLE STREAM---"
FOOTER_TAG = "---END MATHESIS TUPLE STREAM---"

class MathesisBridge:
    @staticmethod
    def pack_program(binary_path: str) -> str:
        """Empaqueta un archivo binario .mat en una cápsula compacta para transferencia entre IAs."""
        with open(binary_path, "rb") as f:
            raw_bytes = f.read()

        if len(raw_bytes) % 64 != 0 or len(raw_bytes) == 0:
            raise ValueError(f"Tamano invalido: {len(raw_bytes)} no es multiplo de 64 bytes.")

        num_ops = len(raw_bytes) // 64
        # Obtener dimension de la primera tupla
        dim_d = struct.unpack_from("<H", raw_bytes, 2)[0]
        chk_blake = hashlib.blake2s(raw_bytes).hexdigest()[:16]
        b64_str = base64.b64encode(raw_bytes).decode('ascii')

        capsule = (
            f"{HEADER_TAG}\n"
            f"META: V1.0|OPS:{num_ops}|DIM:{dim_d}|HASH:{chk_blake}\n"
            f"DATA: {b64_str}\n"
            f"{FOOTER_TAG}\n"
        )
        return capsule

    @staticmethod
    def unpack_capsule(capsule_text: str, output_path: str) -> dict:
        """Desempaqueta una cápsula recibida de otra IA y genera el binario ejecutable .mat."""
        if HEADER_TAG not in capsule_text or FOOTER_TAG not in capsule_text:
            raise ValueError("Capsula corrupta o incompleta: faltan etiquetas de inicio/fin.")

        lines = capsule_text.strip().split("\n")
        meta_line = ""
        data_line = ""

        for line in lines:
            line = line.strip()
            if line.startswith("META:"):
                meta_line = line
            elif line.startswith("DATA:"):
                data_line = line[len("DATA:"):].strip()

        if not data_line:
            raise ValueError("No se encontraron datos binarios en la capsula.")

        raw_bytes = base64.b64decode(data_line)
        if len(raw_bytes) % 64 != 0:
            raise ValueError(f"Tamano decodificado corrupto ({len(raw_bytes)} bytes).")

        num_ops = len(raw_bytes) // 64
        calc_blake = hashlib.blake2s(raw_bytes).hexdigest()[:16]

        with open(output_path, "wb") as f:
            f.write(raw_bytes)

        return {
            "output_path": output_path,
            "num_ops": num_ops,
            "size_bytes": len(raw_bytes),
            "blake2s_hash": calc_blake
        }

    @staticmethod
    def execute_in_silicon(binary_path: str, vm_exe: str = r"E:\MATHESIS\bin\mathesis_vm.exe") -> dict:
        """Ejecuta el archivo binario en el silicio físico y devuelve telemetría cruda."""
        if not os.path.exists(vm_exe):
            raise FileNotFoundError(f"VM no encontrada en: {vm_exe}")

        res = subprocess.run([vm_exe, binary_path], capture_output=True, text=True)
        return {
            "exit_code": res.returncode,
            "stdout": res.stdout,
            "stderr": res.stderr,
            "success": res.returncode == 0
        }


if __name__ == "__main__":
    test_src = r"E:\MATHESIS\examples\test_tribunal_sages.mat"
    test_out = r"E:\MATHESIS\examples\transferred_tribunal_sages.mat"

    print("[*] Empaquetando programa para envio inter-IA...")
    capsule = MathesisBridge.pack_program(test_src)
    print("Capsula generada:\n" + capsule)

    print("[*] IA Receptora: Desempaquetando y restaurando silicio...")
    info = MathesisBridge.unpack_capsule(capsule, test_out)
    print(f"Restaurado con exito: {info}")

    print("[*] Ejecutando en silicio físico...")
    exec_res = MathesisBridge.execute_in_silicon(test_out)
    print(exec_res["stdout"])
    print(f"Estado de silicio: Exit Code {exec_res['exit_code']}")
