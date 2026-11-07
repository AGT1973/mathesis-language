"""
MATHESIS CAPSULE FORMAT (.mcap) — Portable Vector State Container
Empaqueta programa + estados tensoriales vivos en un solo archivo transportable.
Extensión: .mcap (Mathesis Capsule)

Formato binario:
┌──────────────────────────────────────────────────────────┐
│ HEADER (128 bytes)                                       │
│  Magic:     "MCAP" (4B)                                  │
│  Version:   uint16 (2B)                                  │
│  N_Instr:   uint16 (2B) — Cantidad de instrucciones .mat │
│  N_Slabs:   uint16 (2B) — Cantidad de vectores guardados │
│  Dim_D:     uint16 (2B) — Dimensión de cada vector       │
│  Checksum:  BLAKE2s 32B del payload completo             │
│  Name:      84 bytes UTF-8 (nombre del programa)         │
├──────────────────────────────────────────────────────────┤
│ SECTION 1: PROGRAMA (.mat embebido)                      │
│  N_Instr × 64 bytes (tuplas binarias exactas)            │
├──────────────────────────────────────────────────────────┤
│ SECTION 2: SLAB TABLE (índice de vectores)               │
│  N_Slabs × 8 bytes: (uint32 slab_id, uint32 byte_offset)│
├──────────────────────────────────────────────────────────┤
│ SECTION 3: VECTOR DATA (tensores FP64 crudos)            │
│  N_Slabs × Dim_D × 8 bytes (IEEE-754 double)            │
└──────────────────────────────────────────────────────────┘

Tamaño típico para D=2048, 10 instrucciones, 6 slabs:
  Header:    128 B
  Programa:  640 B (10 × 64)
  Slab Table: 48 B (6 × 8)
  Vectors:   98,304 B (6 × 2048 × 8)
  TOTAL:     ~97 KB (comprimido con zlib: ~45 KB)

Esto es lo que mandás por mail, por pendrive o por WhatsApp.
"""

import struct
import hashlib
import zlib
import numpy as np
import os
import json

MAGIC = b"MCAP"
VERSION = 1
HEADER_SIZE = 128
HEADER_FMT = "<4sHHHH32s84s"  # 4+2+2+2+2+32+84 = 128

class MathesisCapsule:
    """Contenedor portable para programas + vectores vivos de MATHESIS."""

    def __init__(self, name="mathesis_capsule", dim_d=2048):
        self.name = name
        self.dim_d = dim_d
        self.program_bytes = b""     # Binario .mat embebido
        self.slabs = {}              # {slab_id: np.ndarray de shape (dim_d,)}

    def load_program(self, mat_path):
        """Carga un archivo .mat existente (las instrucciones compiladas)."""
        with open(mat_path, "rb") as f:
            self.program_bytes = f.read()
        n_instr = len(self.program_bytes) // 64
        print(f"[MCAP] Programa cargado: {mat_path} ({n_instr} instrucciones, {len(self.program_bytes)} bytes)")

    def add_slab(self, slab_id, vector):
        """Agrega un vector vivo (tensor FP64 en la variedad S^{D-1})."""
        v = np.ascontiguousarray(vector, dtype=np.float64)
        assert v.shape == (self.dim_d,), f"Vector debe ser de dimensión {self.dim_d}, recibido {v.shape}"
        self.slabs[slab_id] = v

    def add_random_slab(self, slab_id):
        """Genera un vector aleatorio normalizado en S^{D-1} (para demos)."""
        v = np.random.randn(self.dim_d)
        v /= np.linalg.norm(v)
        self.slabs[slab_id] = v

    def save(self, output_path, compress=True):
        """Empaqueta todo en un archivo .mcap portable."""
        n_instr = len(self.program_bytes) // 64
        n_slabs = len(self.slabs)

        # Section 1: Program bytes
        sec1 = self.program_bytes

        # Section 2: Slab table (slab_id, byte_offset)
        slab_ids = sorted(self.slabs.keys())
        sec2 = b""
        offset = 0
        for sid in slab_ids:
            sec2 += struct.pack("<II", sid, offset)
            offset += self.dim_d * 8

        # Section 3: Vector data
        sec3 = b""
        for sid in slab_ids:
            sec3 += self.slabs[sid].tobytes()

        payload = sec1 + sec2 + sec3

        # BLAKE2s checksum
        checksum = hashlib.blake2s(payload, digest_size=32).digest()

        # Header
        name_bytes = self.name.encode("utf-8")[:84].ljust(84, b"\x00")
        header = struct.pack(HEADER_FMT, MAGIC, VERSION, n_instr, n_slabs, self.dim_d, checksum, name_bytes)
        assert len(header) == HEADER_SIZE

        full_data = header + payload

        if compress:
            compressed = zlib.compress(full_data, level=9)
            with open(output_path, "wb") as f:
                # Prefix with "MCPZ" to indicate zlib-compressed capsule
                f.write(b"MCPZ" + struct.pack("<I", len(full_data)) + compressed)
            raw_kb = len(full_data) / 1024
            comp_kb = (len(compressed) + 8) / 1024
            ratio = comp_kb / raw_kb * 100
            print(f"[MCAP] Cápsula guardada (COMPRIMIDA): {output_path}")
            print(f"  Sin comprimir: {raw_kb:.1f} KB | Comprimido: {comp_kb:.1f} KB ({ratio:.0f}%)")
        else:
            with open(output_path, "wb") as f:
                f.write(full_data)
            print(f"[MCAP] Cápsula guardada (sin comprimir): {output_path} ({len(full_data)/1024:.1f} KB)")

        print(f"  Programa: {n_instr} instrucciones ({len(sec1)} B)")
        print(f"  Vectores: {n_slabs} slabs × D={self.dim_d} ({len(sec3)} B)")
        print(f"  BLAKE2s:  {checksum.hex()[:32]}...")
        return output_path

    @classmethod
    def load(cls, capsule_path):
        """Desempaqueta un archivo .mcap y restaura programa + vectores."""
        with open(capsule_path, "rb") as f:
            raw = f.read()

        # Check if compressed
        if raw[:4] == b"MCPZ":
            original_size = struct.unpack("<I", raw[4:8])[0]
            data = zlib.decompress(raw[8:])
            print(f"[MCAP] Descomprimido: {len(raw)/1024:.1f} KB -> {len(data)/1024:.1f} KB")
        else:
            data = raw

        # Parse header
        header = data[:HEADER_SIZE]
        magic, version, n_instr, n_slabs, dim_d, checksum, name_raw = struct.unpack(HEADER_FMT, header)
        assert magic == MAGIC, f"Archivo no es una cápsula MATHESIS: {magic}"
        name = name_raw.rstrip(b"\x00").decode("utf-8")

        payload = data[HEADER_SIZE:]

        # Verify BLAKE2s
        actual_checksum = hashlib.blake2s(payload, digest_size=32).digest()
        if actual_checksum != checksum:
            raise ValueError("CHECKSUM BLAKE2s FALLIDO — Cápsula corrupta o adulterada")
        print(f"[MCAP] BLAKE2s verificado OK — Integridad certificada")

        # Extract sections
        sec1_size = n_instr * 64
        sec2_size = n_slabs * 8
        sec3_size = n_slabs * dim_d * 8

        program_bytes = payload[:sec1_size]
        slab_table_raw = payload[sec1_size:sec1_size + sec2_size]
        vector_data = payload[sec1_size + sec2_size:]

        # Rebuild capsule
        capsule = cls(name=name, dim_d=dim_d)
        capsule.program_bytes = program_bytes

        for i in range(n_slabs):
            sid, boff = struct.unpack("<II", slab_table_raw[i*8:(i+1)*8])
            vec = np.frombuffer(vector_data[boff:boff + dim_d * 8], dtype=np.float64).copy()
            capsule.slabs[sid] = vec

        print(f"[MCAP] Cápsula restaurada: '{name}'")
        print(f"  Programa: {n_instr} instrucciones")
        print(f"  Vectores: {n_slabs} slabs × D={dim_d}")
        for sid, v in capsule.slabs.items():
            norm = np.linalg.norm(v)
            print(f"    SLAB {sid}: norma = {norm:.15f} (drift = {abs(norm - 1.0):.2e})")

        return capsule

    def extract_program(self, output_mat_path):
        """Extrae el .mat embebido para ejecutar directamente en la VM."""
        with open(output_mat_path, "wb") as f:
            f.write(self.program_bytes)
        print(f"[MCAP] Programa extraído: {output_mat_path}")


# ==================== DEMO: Empaquetar ECO-MATHESIS ====================
if __name__ == "__main__":
    print("=" * 60)
    print("MATHESIS CAPSULE (.mcap) — DEMO DE EMPAQUETADO Y TRANSPORTE")
    print("=" * 60)

    cap = MathesisCapsule(name="ECO-MATHESIS Lotka-Volterra", dim_d=2048)

    # Cargar el programa compilado
    cap.load_program(r"E:\MATHESIS\apps\eco_mathesis.mat")

    # Simular los vectores vivos que estaban en RAM
    np.random.seed(42)
    for slab_id in [10, 11, 12, 13, 14, 15]:
        cap.add_random_slab(slab_id)

    # Guardar la cápsula comprimida
    out = cap.save(r"E:\MATHESIS\apps\eco_mathesis.mcap", compress=True)

    print("\n" + "=" * 60)
    print("RESTAURACIÓN DESDE CÁPSULA (Simula pendrive/email)")
    print("=" * 60)

    # Restaurar desde archivo
    restored = MathesisCapsule.load(out)
    restored.extract_program(r"E:\MATHESIS\apps\eco_restored.mat")

    # Verificar que el .mat extraído es idéntico
    with open(r"E:\MATHESIS\apps\eco_mathesis.mat", "rb") as f1:
        orig = f1.read()
    with open(r"E:\MATHESIS\apps\eco_restored.mat", "rb") as f2:
        rest = f2.read()
    print(f"\nVerificación byte-a-byte: {'IDÉNTICO ✅' if orig == rest else 'DIFERENTE ❌'}")
    print(f"Tamaño .mcap para enviar por mail: {os.path.getsize(out):,} bytes ({os.path.getsize(out)/1024:.1f} KB)")
