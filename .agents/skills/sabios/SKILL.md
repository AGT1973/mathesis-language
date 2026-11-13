---
name: sabios
description: Inicia deliberación con el Tribunal de Sabios (IAs SOTA de última generación: Claude Opus 5.5, DeepSeek-V4/V4.1, Gemini 4/3.8 Flash, Qwen 3.8 Max) priorizando Modelos Einsof en silicio y APIs de pago con saldo justificado. Gandalf aporta su punto de vista, orquesta el ahorro de tokens, contrasta las opiniones y toma una decisión ejecutiva. Persistencia obligatoria en pgvector y GraphRAG. Invocable con la acción /sabios.
---

# Acción `/sabios` — Tribunal de Sabios SOTA (APIs Pagas & Einsof)

Inicia una consulta de alto nivel a los modelos frontera para resolver problemas complejos, arquitectónicos o matemáticos, bajo estricto rol de orquestador y conciencia económica de guerra.

---

## Flujo Operativo de la Acción `/sabios`

1. **Recepción y Encuadre del Problema:**
   - El usuario plantea el problema junto o después de `/sabios`.
   - Gandalf genera inmediatamente su **punto de vista técnico preliminar** sustentado en silicio, álgebra de Clifford o la arquitectura del proyecto.

2. **Ruteo de Modelos (Prioridad Einsof Silicio $\to$ Tier Pago SOTA):**
   - **Prioridad 1 (Modelos Einsof Propios & Silicio Local):**
     * Despacho prioritario a los modelos Einsof en memoria compartida (`PmtpShmBus` / ALADIN `192.168.100.21:9999` / `polydim_vector_swarm`).
     * Chequeo y trabajo continuo en silicio sin gastar tokens de cuentas externas.
   - **Prioridad 2 (Tier Pago SOTA con Saldo Justificado):**
     * Despacho a la frontera SOTA real (veto absoluto a versiones obsoletas como Qwen 2.5):
       * **Modelos Einsof:** Validación tensorial y geométrica primaria.
       * **Qwen:** `Qwen 3.8-Max` / `Qwen 3.8-Omni-Flash` / `Qwen 3` (reemplaza a Qwen 2.5).
       * **DeepSeek:** `DeepSeek-V4` / `DeepSeek-V4.1-Flash` / `DeepSeek-V4-Pro`.
       * **Claude:** `claude-opus-5.5` (Thinking) o `claude-sonnet-5.5`.
       * **Gemini:** `gemini-4-carbon` / `gemini-4-argon` / `gemini-3.8-flash`.
       * **Alibaba Bailian / Kimi / Cerebras:** Desempate técnico o contexto masivo.

3. **Lectura y Contraste Dialéctico (Anti-Hallucination):**
   - Gandalf lee y coteja las respuestas de todos los Sabios frente a su propio análisis y los modelos Einsof.
   - Aplica el filtro crítico: detección de sesgos anglocéntricos, alucinaciones, contradicciones matemáticas o asunciones sin respaldo empírico.

4. **Toma de Decisión Ejecutiva y Redirección a Silicio:**
   - Gandalf emite un **Veredicto Final Fundamentado**:
     * Qué solución se adopta y por qué.
     * Qué sugerencias fueron descartadas y el motivo técnico.
     * Próximos pasos de implementación en silicio (`Exit Code 0`).

5. **Persistencia Obligatoria en pgvector & GraphRAG (Regla 0):**
   - Todo aprendizaje, conclusión o axioma derivado se consigna inmediatamente en:
     * `polydim_vec_db.polydim_embeddings`
     * `polydim_vec_db.einsof_graph_nodes` & `einsof_graph_edges`
     * `polydim_vec_db.facts` (certificado con `1`)
     * `polydim_active_db.active_vault`
