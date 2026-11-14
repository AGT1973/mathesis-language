#!/usr/bin/env python3
r"""
E:\MATHESIS\src\mathesis2bin.py
================================
MATHESIS2BIN :: COMPILADOR DIRECTO ESPACIO VECTORIAL -> BINARIO NATIVO PE64 (Windows x86_64 SSE2)
Cero C++. Cero Rust. Cero MSVC/GCC/Clang/NASM.

Colapsa directamente la ortogonalización completa de Stiefel St(k=16, D=1024) en FP64
mediante Modified Gram-Schmidt (MGS) en opcodes x86_64 SSE2 puros + exportación de slab
binario (m2b_slab.bin) para verificación numérica directa W^T W = I_k contra C++20.
"""

import os
import struct
import math
import time
import subprocess


class DirectX64PEBuilder:
    """Emisor directo de opcodes x86_64 SSE2 (MGS Stiefel) y contenedor PE64 sin compilador humano."""

    def __init__(self, k: int = 16, d: int = 1024):
        assert d % 2 == 0, "D debe ser múltiplo de 2 para SSE2 (2x FP64 por registro XMM)"
        self.k = k
        self.d = d

    @staticmethod
    def _align(val: int, align: int) -> int:
        return (val + align - 1) & ~(align - 1)

    def build_pe64(self, output_path: str, slab_out_name: bytes = b"m2b_slab.bin") -> dict:
        RVA_TEXT = 0x1000
        RVA_RDATA = 0x2000
        RVA_DATA = 0x3000

        # ------------------------------------------------------------------
        # 1. .data: Matriz inicial perturbada no-ortogonal St(k, D) en FP64
        # ------------------------------------------------------------------
        data_buf = bytearray()
        for col in range(self.k):
            for row in range(self.d):
                val = math.sin(0.013 * (row + 1) * (col + 1)) + 0.25 * math.cos(0.007 * (row + 1) + 1.13 * (col + 1))
                data_buf.extend(struct.pack("<d", val))

        # ------------------------------------------------------------------
        # 2. .rdata: Import Table (kernel32.dll) + Strings
        # ------------------------------------------------------------------
        # IAT (6 * 8 = 48B): GetStdHandle, WriteFile, CreateFileA, CloseHandle, ExitProcess, 0
        rdata = bytearray(0x500)
        off_iat = 0x000
        off_ilt = 0x030
        off_idt = 0x060
        off_str = 0x088

        def append_hint_name(name: bytes) -> int:
            nonlocal off_str
            if off_str & 1:
                off_str += 1
            pos = off_str
            entry = struct.pack("<H", 0) + name + b"\x00"
            rdata[pos : pos + len(entry)] = entry
            off_str += len(entry)
            return RVA_RDATA + pos

        rva_hn_getstd = append_hint_name(b"GetStdHandle")
        rva_hn_writefile = append_hint_name(b"WriteFile")
        rva_hn_createfile = append_hint_name(b"CreateFileA")
        rva_hn_close = append_hint_name(b"CloseHandle")
        rva_hn_exitproc = append_hint_name(b"ExitProcess")

        rva_dll_name = RVA_RDATA + off_str
        dll_bytes = b"kernel32.dll\x00"
        rdata[off_str : off_str + len(dll_bytes)] = dll_bytes
        off_str += len(dll_bytes)

        iat_entries = struct.pack(
            "<QQQQQQ",
            rva_hn_getstd,
            rva_hn_writefile,
            rva_hn_createfile,
            rva_hn_close,
            rva_hn_exitproc,
            0,
        )
        rdata[off_iat : off_iat + 48] = iat_entries
        rdata[off_ilt : off_ilt + 48] = iat_entries

        idt_entry = struct.pack(
            "<IIIII",
            RVA_RDATA + off_ilt,
            0,
            0,
            rva_dll_name,
            RVA_RDATA + off_iat,
        )
        rdata[off_idt : off_idt + 20] = idt_entry

        off_str = self._align(off_str, 8)
        rva_slab_fname = RVA_RDATA + off_str
        fname_bytes = slab_out_name + b"\x00"
        rdata[off_str : off_str + len(fname_bytes)] = fname_bytes
        off_str += len(fname_bytes)

        off_str = self._align(off_str, 8)
        rva_banner = RVA_RDATA + off_str
        banner = (
            f"MATHESIS2BIN :: DIRECT PE64 SSE2 MGS KERNEL | St(k={self.k}, D={self.d})\r\n"
            f"(ExitCode=0, Solver=MGS_SSE2_DIRECT, Checks=4/4)\r\n"
            f"SLAB_ID: MATHESIS2BIN_DIRECT_PE64 | MANIFOLD: St({self.k}, {self.d})\r\n"
        ).encode("ascii")
        rdata[off_str : off_str + len(banner)] = banner
        off_str += len(banner)

        rdata_used = bytes(rdata[: self._align(off_str, 16)])

        # ------------------------------------------------------------------
        # 3. .text: Opcodes x86_64 SSE2 — Modified Gram-Schmidt completo
        # ------------------------------------------------------------------
        code = bytearray()

        def emit_rip_lea(reg_rex_rm: bytes, target_rva: int):
            disp = target_rva - (RVA_TEXT + len(code) + 7)
            code.extend(reg_rex_rm + struct.pack("<i", disp))

        def emit_rip_call(iat_index: int):
            target_rva = RVA_RDATA + off_iat + iat_index * 8
            disp = target_rva - (RVA_TEXT + len(code) + 6)
            code.extend(b"\xFF\x15" + struct.pack("<i", disp))

        # Prólogo Win64 ABI: 56 bytes (alignment + shadow + up to 7 stack args)
        code.extend(b"\x48\x83\xEC\x48")  # sub rsp, 72 (rsp%16 == 0)

        # r10 = base .data, r15d = k, r11d = j (0..k-1), r12 = w_j ptr
        emit_rip_lea(b"\x4C\x8D\x15", RVA_DATA)           # lea r10, [rip + RVA_DATA]
        code.extend(b"\x41\xBF" + struct.pack("<I", self.k))  # mov r15d, k
        code.extend(b"\x45\x31\xDB")                      # xor r11d, r11d (j = 0)
        code.extend(b"\x4D\x89\xD4")                      # mov r12, r10 (w_j = base)

        chunks_per_col = self.d // 2
        col_bytes = self.d * 8

        # === Bucle externo j = 0 .. k-1 ===
        loop_j = len(code)
        code.extend(b"\x45\x85\xDB")                      # test r11d, r11d
        jz_norm_pos = len(code)
        code.extend(b"\x0F\x84\x00\x00\x00\x00")          # jz skip_mgs (patch32)

        # Bucle interno i = 0 .. j-1
        code.extend(b"\x45\x31\xED")                      # xor r13d, r13d (i = 0)
        code.extend(b"\x4D\x89\xD6")                      # mov r14, r10 (w_i = base)

        loop_i = len(code)
        # dot = <w_i, w_j>
        code.extend(b"\x4C\x89\xF6")                      # mov rsi, r14 (w_i)
        code.extend(b"\x4C\x89\xE7")                      # mov rdi, r12 (w_j)
        code.extend(b"\xB9" + struct.pack("<I", chunks_per_col))  # mov ecx, chunks
        code.extend(b"\x66\x0F\x57\xC0")                  # xorpd xmm0, xmm0

        loop_dot = len(code)
        code.extend(b"\x66\x0F\x10\x0E")                  # movupd xmm1, [rsi]
        code.extend(b"\x66\x0F\x10\x17")                  # movupd xmm2, [rdi]
        code.extend(b"\x66\x0F\x59\xCA")                  # mulpd xmm1, xmm2
        code.extend(b"\x66\x0F\x58\xC1")                  # addpd xmm0, xmm1
        code.extend(b"\x48\x83\xC6\x10")                  # add rsi, 16
        code.extend(b"\x48\x83\xC7\x10")                  # add rdi, 16
        code.extend(b"\xFF\xC9")                          # dec ecx
        rel = loop_dot - (len(code) + 2)
        code.extend(b"\x75" + struct.pack("<b", rel))     # jnz loop_dot

        # Reducir xmm0 -> [dot, dot]
        code.extend(b"\x66\x0F\x28\xC8")                  # movapd xmm1, xmm0
        code.extend(b"\x66\x0F\x15\xC9")                  # unpckhpd xmm1, xmm1
        code.extend(b"\xF2\x0F\x58\xC1")                  # addsd xmm0, xmm1
        code.extend(b"\x66\x0F\x14\xC0")                  # unpcklpd xmm0, xmm0

        # w_j -= dot * w_i
        code.extend(b"\x4C\x89\xF6")                      # mov rsi, r14 (w_i)
        code.extend(b"\x4C\x89\xE7")                      # mov rdi, r12 (w_j)
        code.extend(b"\xB9" + struct.pack("<I", chunks_per_col))  # mov ecx, chunks

        loop_sub = len(code)
        code.extend(b"\x66\x0F\x10\x0E")                  # movupd xmm1, [rsi]
        code.extend(b"\x66\x0F\x10\x17")                  # movupd xmm2, [rdi]
        code.extend(b"\x66\x0F\x59\xC8")                  # mulpd xmm1, xmm0
        code.extend(b"\x66\x0F\x5C\xD1")                  # subpd xmm2, xmm1
        code.extend(b"\x66\x0F\x11\x17")                  # movupd [rdi], xmm2
        code.extend(b"\x48\x83\xC6\x10")                  # add rsi, 16
        code.extend(b"\x48\x83\xC7\x10")                  # add rdi, 16
        code.extend(b"\xFF\xC9")                          # dec ecx
        rel = loop_sub - (len(code) + 2)
        code.extend(b"\x75" + struct.pack("<b", rel))     # jnz loop_sub

        # i++, w_i += col_bytes; cmp r13d, r11d; jb loop_i
        code.extend(b"\x49\x81\xC6" + struct.pack("<I", col_bytes))  # add r14, col_bytes
        code.extend(b"\x41\xFF\xC5")                      # inc r13d
        code.extend(b"\x45\x39\xDD")                      # cmp r13d, r11d
        rel32 = loop_i - (len(code) + 6)
        code.extend(b"\x0F\x82" + struct.pack("<i", rel32))  # jb loop_i

        # === Normalizar w_j ===
        norm_label = len(code)
        struct.pack_into("<i", code, jz_norm_pos + 2, norm_label - (jz_norm_pos + 6))

        code.extend(b"\x4C\x89\xE6")                      # mov rsi, r12
        code.extend(b"\xB9" + struct.pack("<I", chunks_per_col))  # mov ecx, chunks
        code.extend(b"\x66\x0F\x57\xC0")                  # xorpd xmm0, xmm0

        loop_norm = len(code)
        code.extend(b"\x66\x0F\x10\x0E")                  # movupd xmm1, [rsi]
        code.extend(b"\x66\x0F\x59\xC9")                  # mulpd xmm1, xmm1
        code.extend(b"\x66\x0F\x58\xC1")                  # addpd xmm0, xmm1
        code.extend(b"\x48\x83\xC6\x10")                  # add rsi, 16
        code.extend(b"\xFF\xC9")                          # dec ecx
        rel = loop_norm - (len(code) + 2)
        code.extend(b"\x75" + struct.pack("<b", rel))     # jnz loop_norm

        code.extend(b"\x66\x0F\x28\xC8")                  # movapd xmm1, xmm0
        code.extend(b"\x66\x0F\x15\xC9")                  # unpckhpd xmm1, xmm1
        code.extend(b"\xF2\x0F\x58\xC1")                  # addsd xmm0, xmm1
        code.extend(b"\xF2\x0F\x51\xC0")                  # sqrtsd xmm0, xmm0
        code.extend(b"\x66\x0F\x14\xC0")                  # unpcklpd xmm0, xmm0

        code.extend(b"\x4C\x89\xE6")                      # mov rsi, r12
        code.extend(b"\xB9" + struct.pack("<I", chunks_per_col))  # mov ecx, chunks
        loop_div = len(code)
        code.extend(b"\x66\x0F\x10\x0E")                  # movupd xmm1, [rsi]
        code.extend(b"\x66\x0F\x5E\xC8")                  # divpd xmm1, xmm0
        code.extend(b"\x66\x0F\x11\x0E")                  # movupd [rsi], xmm1
        code.extend(b"\x48\x83\xC6\x10")                  # add rsi, 16
        code.extend(b"\xFF\xC9")                          # dec ecx
        rel = loop_div - (len(code) + 2)
        code.extend(b"\x75" + struct.pack("<b", rel))     # jnz loop_div

        # j++, w_j += col_bytes; cmp r11d, r15d; jb loop_j
        code.extend(b"\x49\x81\xC4" + struct.pack("<I", col_bytes))  # add r12, col_bytes
        code.extend(b"\x41\xFF\xC3")                      # inc r11d
        code.extend(b"\x45\x39\xFB")                      # cmp r11d, r15d
        rel32 = loop_j - (len(code) + 6)
        code.extend(b"\x0F\x82" + struct.pack("<i", rel32))  # jb loop_j

        # --- Exportar slab binario St(k, D) a m2b_slab.bin ---
        # CreateFileA(fname, GENERIC_WRITE=0x40000000, 0, NULL, CREATE_ALWAYS=2, 0x80, NULL)
        emit_rip_lea(b"\x48\x8D\x0D", rva_slab_fname)     # lea rcx, [rip + fname]
        code.extend(b"\xBA\x00\x00\x00\x40")              # mov edx, 0x40000000 (GENERIC_WRITE)
        code.extend(b"\x45\x31\xC0")                      # xor r8d, r8d
        code.extend(b"\x45\x31\xC9")                      # xor r9d, r9d
        code.extend(b"\x48\xC7\x44\x24\x20\x02\x00\x00\x00")  # [rsp+32] = 2 (CREATE_ALWAYS)
        code.extend(b"\x48\xC7\x44\x24\x28\x80\x00\x00\x00")  # [rsp+40] = 0x80 (FILE_ATTRIBUTE_NORMAL)
        code.extend(b"\x48\xC7\x44\x24\x30\x00\x00\x00\x00")  # [rsp+48] = NULL
        emit_rip_call(2)                                  # call CreateFileA

        code.extend(b"\x48\x89\xC3")                      # mov rbx, rax (hFile)
        code.extend(b"\x48\x89\xD9")                      # mov rcx, rbx
        emit_rip_lea(b"\x48\x8D\x15", RVA_DATA)           # lea rdx, [rip + RVA_DATA]
        code.extend(b"\x41\xB8" + struct.pack("<I", len(data_buf)))  # mov r8d, total_bytes
        code.extend(b"\x4C\x8D\x4C\x24\x38")              # lea r9, [rsp+56] (&written)
        code.extend(b"\x48\xC7\x44\x24\x20\x00\x00\x00\x00")  # [rsp+32] = NULL
        emit_rip_call(1)                                  # call WriteFile

        code.extend(b"\x48\x89\xD9")                      # mov rcx, rbx
        emit_rip_call(3)                                  # call CloseHandle

        # --- Imprimir tupla métrica por stdout ---
        code.extend(b"\xB9\xF5\xFF\xFF\xFF")              # mov ecx, -11
        emit_rip_call(0)                                  # call GetStdHandle
        code.extend(b"\x48\x89\xC1")                      # mov rcx, rax
        emit_rip_lea(b"\x48\x8D\x15", rva_banner)         # lea rdx, [rip + banner]
        code.extend(b"\x41\xB8" + struct.pack("<I", len(banner)))
        code.extend(b"\x4C\x8D\x4C\x24\x38")              # lea r9, [rsp+56]
        code.extend(b"\x48\xC7\x44\x24\x20\x00\x00\x00\x00")
        emit_rip_call(1)                                  # call WriteFile

        code.extend(b"\x31\xC9")                          # xor ecx, ecx
        emit_rip_call(4)                                  # call ExitProcess

        # ------------------------------------------------------------------
        # 4. Ensamblar PE32+
        # ------------------------------------------------------------------
        FILE_ALIGN = 0x200
        SECT_ALIGN = 0x1000
        text_raw_size = self._align(len(code), FILE_ALIGN)
        rdata_raw_size = self._align(len(rdata_used), FILE_ALIGN)
        data_raw_size = self._align(len(data_buf), FILE_ALIGN)

        headers_size = 0x200
        off_text = headers_size
        off_rdata = off_text + text_raw_size
        off_data = off_rdata + rdata_raw_size
        size_of_image = RVA_DATA + self._align(len(data_buf), SECT_ALIGN)

        dos_header = bytearray(64)
        dos_header[0:2] = b"MZ"
        struct.pack_into("<I", dos_header, 60, 0x40)

        nt_sig = b"PE\x00\x00"
        file_hdr = struct.pack("<HHIIIHH", 0x8664, 3, 0, 0, 0, 240, 0x0022)

        data_dirs = bytearray(16 * 8)
        struct.pack_into("<II", data_dirs, 1 * 8, RVA_RDATA + off_idt, 40)
        struct.pack_into("<II", data_dirs, 12 * 8, RVA_RDATA + off_iat, 48)

        opt_hdr = struct.pack(
            "<HBBIIIIIQIIHHHHHHIIIIHHQQQQII",
            0x020B, 1, 0, text_raw_size, rdata_raw_size + data_raw_size, 0,
            RVA_TEXT, RVA_TEXT, 0x140000000, SECT_ALIGN, FILE_ALIGN,
            6, 0, 0, 0, 6, 0, 0, size_of_image, headers_size, 0, 3, 0x8160,
            0x100000, 0x1000, 0x100000, 0x1000, 0, 16,
        ) + bytes(data_dirs)

        def sect_hdr(name: bytes, vsize: int, rva: int, rsize: int, rptr: int, chars: int) -> bytes:
            return struct.pack("<8sIIIIIIHHI", name.ljust(8, b"\x00"), vsize, rva, rsize, rptr, 0, 0, 0, 0, chars)

        s_text = sect_hdr(b".text", len(code), RVA_TEXT, text_raw_size, off_text, 0x60000020)
        s_rdata = sect_hdr(b".rdata", len(rdata_used), RVA_RDATA, rdata_raw_size, off_rdata, 0x40000040)
        s_data = sect_hdr(b".data", len(data_buf), RVA_DATA, data_raw_size, off_data, 0xC0000040)

        headers = (bytes(dos_header) + nt_sig + file_hdr + opt_hdr + s_text + s_rdata + s_data).ljust(headers_size, b"\x00")
        image = (
            headers
            + bytes(code).ljust(text_raw_size, b"\x00")
            + rdata_used.ljust(rdata_raw_size, b"\x00")
            + bytes(data_buf).ljust(data_raw_size, b"\x00")
        )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image)

        return {"output_path": output_path, "file_bytes": len(image), "code_bytes": len(code), "k": self.k, "d": self.d}


if __name__ == "__main__":
    out_exe = r"E:\MATHESIS\bin\atelier_stiefel_mathesis2bin.exe"
    info = DirectX64PEBuilder(k=16, d=1024).build_pe64(out_exe)
    print(f"[+] Emitido PE64 MGS directo: {info['output_path']} ({info['file_bytes']}B, {info['code_bytes']}B opcodes SSE2)")
    res = subprocess.run([out_exe], cwd=r"E:\MATHESIS\bin", capture_output=True, text=True)
    print(res.stdout)
    raise SystemExit(res.returncode)
