---
name: limpiar
description: Protocolo de Saneamiento y Compactación Contextual (/compact + Checkpoint + Handover Prompt). Recomienda /compact al inicio, persiste el estado atómico en PostgreSQL 16 y genera un resumen ejecutivo junto con un prompt de migración listo para copiar y pegar en una nueva conversación o continuar sin amnesia.
---

# /limpiar — Protocolo de Saneamiento y Compactación Contextual

**Trigger**: `/limpiar` o `/Limpiar`

**Doctrina**: Libera espacio en la ventana de contexto de la conversación. Inicia recomendando `/compact`, ejecuta la captura atómica en silicio (PostgreSQL 16 pgvector & GraphRAG) y finaliza generando tanto un resumen ejecutivo como el **prompt exacto de migración** para iniciar un nuevo chat o continuar sin amnesia.

## Flujo de Ejecución Secuencial

### Paso 1: Recomendación Inmediata de `/compact`
Al invocarse `/limpiar`, el agente debe indicar explícitamente al inicio la ejecución de la barra de comando:
> *"Iniciando protocolo `/limpiar`. Se sugiere ejecutar `/compact` para podar el historial de tokens local mientras se consolida la memoria persistente."*

### Paso 2: Captura y Persistencia del Estado Atómico
Recopilar la tupla de estado actual:
- **Métricas empíricas**: Ahorro de tokens, latencias, Exit Codes de la sesión.
- **Artefactos y Código**: Teoremas, kernels FFI (C++/Rust/Triton), scripts o tablas modificadas.
- **Git & Worktree**: Estado de branches, commits pendientes y rutas de backup en `_HISTORICO`.
- **Persistencia en PostgreSQL 16**:
  * Actualizar `polydim_vec_db.session_context`.
  * Insertar hecho certificado en `polydim_vec_db.facts` (fact_type='checkpoint').
  * Actualizar `polydim_active_db.active_vault` (`SESSION_CHECKPOINT_LATEST`).
  * Apéndice en `E:\POLYDIM-THEORETICAL\contexto_historico.md`.

### Paso 3: Resumen Ejecutivo de la Conversación
Emitir un bloque markdown conciso con:
- Objetivos solicitados por Ariel durante la sesión.
- Tareas completadas con verificación empírica (Exit Code 0).
- Decisiones arquitectónicas o reglas adoptadas.

### Paso 4: Generación del Prompt de Migración (Handover Block)
Entregar al final un bloque de código markdown listo para copiar, diseñado para abrir una nueva sesión en Antigravity y reanudar inmediatamente sin pérdida de rumbo:

````markdown
```markdown
Hola Gandalf. Continuamos con el trabajo de POLYDIM-EINSOF.
Estado de la sesión anterior:
- Contexto persistido en PostgreSQL 16 (session_context y active_vault).
- Últimos hitos: <resumen de 2-3 líneas>
- Archivos y kernels activos: <rutas principales>
- Tarea inmediata / Siguiente paso: <acción concreta a ejecutar>
Bootstrap automático: Ejecuta `SELECT * FROM v_bootstrap_summary;` y continúa.
```
````
