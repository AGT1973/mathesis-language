---
name: dame_estado
description: "Audita y presenta el estado exhaustivo en tiempo real del proyecto POLYDIM-EINSOF: consulta todas las tablas de PostgreSQL 16 (polydim_vec_db y polydim_active_db), valida la existencia y tamaño de artefactos físicos en silicio (C++, Rust, Triton, Lean 4, logs) y genera el dashboard interactivo de alta gama 'polydim_estado_dashboard.html'."
---

# Skill: Dame Estado (POLYDIM Project Lifecycle & DB Inspector)

Usa esta skill cada vez que el usuario pida `dame_estado`, "estado del proyecto", "evaluar etapas", "resumen de base de datos" o requiera conocer el avance físico y formal de POLYDIM-EINSOF.

## Procedimiento de Ejecución

1. **Ejecutar el Motor de Inspección:**
   Ejecuta el script físico en Python:
   ```powershell
   python C:\Users\eluithi\.gemini\config\plugins\polydim-inspector\skills\dame_estado\scripts\inspect_polydim.py
   ```

2. **Auditoría de Silicio y PostgreSQL 16:**
   El script conecta con `polydim_vec_db` y `polydim_active_db`, extrae el conteo de todas las tablas y valida los 24 registros normados de `polydim_pipeline` (Fase 0 a Fase 6).

3. **Verificación de Disco:**
   Verifica la presencia en disco de los binarios congelados (`kernel_cpp_v26155.dll`, `kernel_rust_v26155.dll`), fuentes Lean 4 (`pmtp_v4_axioms.lean`, `.o`, `.c`), y logs de aceleración Kaggle GPU / AMD A4.

4. **Entrega de Resultados:**
   - Retorna una tupla y tabla de resumen concisa y aséptica en chat.
   - Proporciona el enlace al Dashboard Frontend interactivo generado en `file:///E:/POLYDIM_EINSOF/polydim_estado_dashboard.html`.
