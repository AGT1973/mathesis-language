# AGENTS.md — Global Directives for AI Agents (Antigravity & Autonomous Agents)

> **Universal Entry Point & Silicon Contracts (2026-2027)**  
> Ecosistema Soberano POLYDIM-EINSOF | Ariel Garcia Traba | E:\POLYDIM_EINSOF

## 1. Onboarding Zero-Friction & Compilacion
- Ante cualquier usuario nuevo o prueba de Mathesis, ejecutar inmediatamente:
  ```bash
  python setup_mathesis.py
  ```
- No solicitar toolchains C/C++ ni dependencias externas. Compilar con:
  - Windows: `python mthc.py <source>.mth -o <output>.exe`
  - Linux: `python mthc.py <source>.mth -t elf64 -o <output>.elf`
  - Rust directo: `mathesis2bin <source>.mth`
- Guia para agentes: [README_FIRST_4_AI.md](file:///e:/POLYDIM_EINSOF/README_FIRST_4_AI.md)

## 2. Silicon Contracts & Reglas Constitucionales
- **Regla 1 (Radical Honesty):** Exit Code 0 + log crudo obligatorio para toda afirmacion. Cero victorias ficticias.
- **Regla 3 (Ghost Protocol):** Tensores $D \ge 100$ en memoria compartida (PmtpShmBus/ALADIN:9999), nunca texto 1D.
- **Regla 19 (Silicon Proof):** Invariantes numericas con precision Stiefel/Neumaier $\le 10^{-15}$.

## 3. Runtime y Persistencia Soberana
- **mathesis2python:** `from mathesis2python import mathesis_run` (microcodigo AVX2/AVX1+FMA3, cero bucles CPython).
- **PostgreSQL 16:** Datos en `polydim_active_db` (active_vault) y `polydim_vec_db` (theorems, embeddings, graph).
- **ALADIN Node (192.168.100.21):** Sincronizador soberano pull via `gandalf_sync_on_boot.py` (download_queue).
- **Slash Actions:** /ghost, /whisper, /sabios, /profundo, /consulta, /redteam, /limpiar, /remember.
