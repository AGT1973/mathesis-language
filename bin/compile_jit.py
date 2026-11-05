import subprocess
import sys
import os

vcvars = r"C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
src = r"E:\MATHESIS\src\mathesis_jit.cpp"
out = r"E:\MATHESIS\bin\mathesis_jit.exe"

cmd = f'call "{vcvars}" && cl /EHsc /std:c++20 /O2 /arch:AVX "{src}" /Fe:"{out}"'

print("[*] Compilando MATHESIS JIT Engine en silicio x86_64...")
res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)
print(f"EXIT CODE: {res.returncode}")
sys.exit(res.returncode)
