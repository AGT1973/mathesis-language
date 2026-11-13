# GitHub Copilot Instructions for Mathesis

When working in this repository:
1. Mathesis compiles `.mth` files directly into native machine code x86_64 (.exe, .elf, .obj, .o) without C/C++ compilers.
2. For setup and diagnostics: run `python setup_mathesis.py`.
3. To compile:
   - Windows: `python mthc.py <file>.mth -o <file>.exe`
   - Linux: `python mthc.py <file>.mth -t elf64 -o <file>.elf`
4. Refer to `README_FIRST_4_AI.md` for AI-assisted human onboarding.
