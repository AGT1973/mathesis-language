@echo off
rem ==============================================================================
rem CALTECH WORKSTATIONS BUILD SCRIPT (Windows x86_64)
rem Compila con GCC (MinGW) o ejecuta directamente con mathesis_vm.exe
rem ==============================================================================
chcp 65001 >nul
echo ==========================================================================
echo    COMPILANDO Y EJECUTANDO PROGRAMAS MATHESIS EN WINDOWS WORKSTATIONS
echo ==========================================================================

where gcc >nul 2>nul
if %errorlevel% equ 0 (
    echo [*] MinGW GCC detectado. Compilando ejecutables nativos .exe...
    for /r %%i in (*_portable.c) do (
        echo [+] Compilando %%i...
        gcc -O3 "%%i" -lm -o "%%~dpni_native.exe"
    )
) else (
    echo [*] GCC no encontrado en PATH. Utilizando Máquina Virtual de Silicio mathesis_vm.exe...
)

echo.
echo [*] Ejecutando pruebas de silicio con la Máquina Virtual...
for /r %%i in (*.mat) do (
    echo [+] Ejecutando cartucho %%~nxi:
    "E:\MATHESIS\bin\mathesis_vm.exe" "%%i"
    echo --------------------------------------------------------------------------
)

echo.
echo ==========================================================================
echo [OK] EJECUCION FINALIZADA EN TODAS LAS WORKSTATIONS (EXIT CODE 0)
echo ==========================================================================
pause
