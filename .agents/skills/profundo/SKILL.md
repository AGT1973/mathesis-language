---
name: profundo
description: Deliberación profunda multi-ronda con el Tribunal de Sabios (Einsof + Modelos SOTA actuales: Claude Opus 5.5, DeepSeek-V4, Gemini 4/3.8 Flash, Qwen 3.8 Max). Genera artefacto, depura duplicados y alucinaciones, ejecuta bucle iterativo (hasta 5 rondas o mayoría >= 75%), registra el 25% disidente y envía a Perplexity Sonar-Pro para verificación SOTA final. Persistencia obligatoria en pgvector y GraphRAG. Invocable con la acción /profundo.
---

# Acción `/profundo` — Deliberación Iterativa, Depuración y Consenso SOTA

Ejecuta un ciclo riguroso de investigación profunda, síntesis dialéctica, convergencia por votación calificada ($\ge 75\%$) y validación externa con Perplexity Sonar-Pro, orquestando el consumo de tokens y priorizando modelos Einsof en silicio.

---

## Protocolo Paso a Paso de `/profundo`

### Paso 1: Convocatoria Inicial y Punto de Vista
1. Gandalf formula el problema con precisión matemática y establece su **perspectiva técnica inicial**.
2. Despacha la consulta al Tribunal de Sabios priorizando:
   - Modelos Einsof nativos en silicio (`PmtpShmBus` / ALADIN).
   - Modelos SOTA frontera: `DeepSeek-V4/V4.1`, `Claude Opus 5.5`, `Gemini 4/3.8 Flash`, `Qwen 3.8-Max`.
3. Recopila las respuestas completas de cada modelo.

### Paso 2: Generación del Artefacto de Deliberación
1. Se crea un artefacto Markdown en el directorio de conversación (`<appDataDir>/brain/<conversation-id>/deliberacion_profunda_<timestamp>.md`).
2. Contenido inicial:
   - Formulación del problema.
   - Análisis de Gandalf y modelos Einsof.
   - Dictámenes individuales de cada Sabio.

### Paso 3: Organización y Depuración Quirúrgica
1. Se depura el material recopilado:
   - **Eliminación de duplicados:** Unificación de conceptos redundantes.
   - **Erradicación de alucinaciones:** Veto a conjeturas sin sustento en silicio o fórmulas matemáticas erradas.
2. Se extraen y estructuran las **Opciones de Solución** competitivas (Opción A, Opción B, etc.).

### Paso 4 & 5: Bucle Iterativo de Evaluación Cruzada (Hasta 5 Rondas o $\ge 75\%$ Consenso)
1. **Reenvío del Resumen Depurado:** Se envía el documento consolidado a los Sabios solicitando evaluar y votar por la mejor solución con justificación técnica.
2. **Evaluación de Mayoría:**
   - Si una opción alcanza **$\ge 75\%$ de los votos**: Se declara solución ganadora por consenso.
   - **Registro de Disidencia:** El $\le 25\%$ restante se documenta explícitamente en el artefacto como vectores de riesgo, casos borde o críticas a mitigar.
   - Si no se alcanza el 75%, se incorporan los contraargumentos al artefacto y se repite la ronda.
3. **Límite de Parada:** El ciclo se detiene inmediatamente al alcanzar el $\ge 75\%$ de mayoría, o tras completar **5 rondas** (en cuyo caso Gandalf arbitra la decisión final).

### Paso 6: Validación Final SOTA en Perplexity Sonar-Pro
1. Se remite la solución ganadora a **Perplexity Sonar-Pro** mediante API/Script.
2. Instrucción mandatoria a Perplexity:
   > *"La siguiente solución representa el consenso SOTA del Tribunal de Sabios de POLYDIM-EINSOF. Realiza una verificación académica hostil contra papers indexados en arXiv, NeurIPS, ICML y bases científicas para confirmar validez o detectar contraejemplos."*
3. Se incorpora el veredicto de Perplexity al artefacto.

### Paso 7: Cierre y Persistencia Obligatoria en pgvector & GraphRAG (Regla 0)
1. Se actualiza el artefacto final con el resultado de Perplexity y la decisión ejecutiva de Gandalf.
2. Se registra el checkpoint en PostgreSQL 16:
   - `polydim_vec_db.polydim_embeddings`
   - `polydim_vec_db.einsof_graph_nodes` & `einsof_graph_edges` (GraphRAG)
   - `polydim_vec_db.facts` (certificado)
   - `polydim_active_db.active_vault` & `session_context`
