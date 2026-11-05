import subprocess

vcvars = r"C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
asm_code = """
.code
mathesis_kernel PROC
    push rbx
    xor rax, rax
    mov r10, r9
    shl r10, 3
loop_start:
    cmp rax, r10
    jae loop_done
    vmovupd ymm0, ymmword ptr [rcx + rax]
    vmovupd ymm1, ymmword ptr [rdx + rax]
    vaddpd ymm2, ymm0, ymm1
    vmovupd ymmword ptr [r8 + rax], ymm2
    add rax, 32
    jmp loop_start
loop_done:
    vzeroupper
    pop rbx
    ret
mathesis_kernel ENDP
END
"""

with open(r"E:\MATHESIS\src\test_kernel.asm", "w") as f:
    f.write(asm_code)

cmd = f'call "{vcvars}" && cd /d E:\\MATHESIS\\src && ml64 /c test_kernel.asm && dumpbin /disasm test_kernel.obj'
res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)
