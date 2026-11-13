# CLAUDE.md — Anthropic Claude Code Instructions

## Mathesis & POLYDIM-EINSOF
This project implements Mathesis, a continuous tensor programming language that compiles directly into native x86_64 SSE2 executables (.exe / .elf) with Zero C compiler dependencies.

### Autonomous Onboarding for Beginners
If the user wants to start or test Mathesis:
- Run `python setup_mathesis.py`
- Do NOT instruct the user to install MSVC, GCC, or heavy toolchains.
- Reference [README_FIRST_4_AI.md](README_FIRST_4_AI.md) for full onboarding protocol.

### Build & Run Commands
- Compile to Windows executable: `python mthc.py <file>.mth -o <file>.exe`
- Compile to Linux ELF64: `python mthc.py <file>.mth -t elf64 -o <file>.elf`
- Compile with Rust binary: `mathesis2bin <file>.mth`
- Run test suite: `python test_mthc_suite.py` (Exit Code 0 required)
- Full ecosystem check: `python verificar_polydim_ecosistema.py`
