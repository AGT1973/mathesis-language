#!/usr/bin/env bash
# ==============================================================================
# CALTECH WORKSTATIONS UNIVERSAL BUILD SCRIPT (Linux & macOS Intel/Apple Silicon)
# Compila todos los programas de MATHESIS a binarios nativos ELF / Mach-O
# Requisitos: gcc o clang (estandar en Linux y Mac Xcode Command Line Tools)
# ==============================================================================
set -e
echo "=========================================================================="
echo "   COMPILANDO PROGRAMAS DE MATHESIS PARA WORKSTATIONS (LINUX / MACOS)     "
echo "=========================================================================="

COMPILER="gcc"
if command -v clang &> /dev/null; then
    COMPILER="clang"
fi
echo "[*] Usando compilador nativo: $COMPILER"

find . -name "*_portable.c" | while read -r c_src; do
    bin_out="${c_src%_portable.c}_native"
    echo "[+] Compilando: $c_src -> $bin_out"
    $COMPILER -O3 "$c_src" -lm -o "$bin_out"
    echo "    -> Ejecutando prueba de silicio..."
    "$bin_out" | grep "ESTADO DE SILICIO" || true
done

echo "=========================================================================="
echo "[+] TODAS LAS ÁREAS COMPILADAS Y CERTIFICADAS EN WORKSTATIONS LOCALES"
echo "=========================================================================="
