
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
