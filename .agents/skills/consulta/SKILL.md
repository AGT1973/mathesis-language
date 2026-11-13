---
name: consulta
description: Consulta rápida y gratuita a IAs de Tier Free SOTA (Groq, SambaNova, AI Studio, Hugging Face, OpenRouter free) priorizando modelos Einsof locales y del nodo ALADIN. Cero consumo de saldo de Ariel. Gandalf orquesta el carrusel de claves, contrasta opiniones y toma una decisión ejecutiva. Persistencia obligatoria en pgvector y GraphRAG. Invocable con la acción /consulta.
---

# Acción `/consulta` — Consulta Tier Free & Einsof Local (0 Saldo)

Permite resolver dudas técnicas, explorar alternativas de código o testear ideas utilizando exclusivamente **recursos gratuitos (Tier Free SOTA) y modelos Einsof en silicio**, protegiendo al 100% el saldo de las cuentas pagas de Ariel.

---

## Flujo Operativo de la Acción `/consulta`

1. **Recepción del Problema:**
   - Se recibe el planteo técnico del usuario.
   - Gandalf expone de forma inmediata su **punto de vista preliminar** de arquitectura o implementación.

2. **Ruteo de Modelos (Prioridad Einsof Local $\to$ Tier Free Pools SOTA):**
   - **Prioridad 1 (Modelos Einsof Propios & ALADIN):**
     * Modelos locales en silicio y en el nodo ALADIN (`192.168.100.21:9999`):
       - Modelos Einsof nativos para trabajo y chequeo continuo.
       - Modelos locales en Ollama / PmtpShmBus (`Qwen 3`, `DeepSeek-V4`).
       - Adaptadores y transformaciones en `PmtpShmBus`.
   - **Prioridad 2 (Tier Free Pools vía MCP Carousel - Modelos SOTA):**
     * **SambaNova (Pools 01 a 10):** `Qwen 3 72B / 3.8-Max`, `DeepSeek-V4-Flash / V4.1`.
     * **Groq (Pools 01 a 10):** `DeepSeek-V4-Flash`, `LLaMA 3.3 70B Versatile`.
     * **Google AI Studio (Pools 01 a 12):** `Gemini 3.8 Flash` / `Gemini 4 Argon`.
     * **Hugging Face / OpenRouter Free:** Modelos abiertos comunitarios de última generación.
   - **Rotación Automática por Cooldown:** Si alguna clave gratuita responde con `HTTP 429`, el carrusel salta automáticamente a la siguiente cuenta del pool sin interrumpir ni gastar un solo centavo de saldo.

3. **Lectura y Contraste de Opiniones:**
   - Gandalf analiza las respuestas recibidas de los modelos libres y locales frente a su hipótesis.
   - Detecta errores de sintaxis, discrepancias o sugerencias de optimización.

4. **Toma de Decisión Ejecutiva:**
   - Gandalf sintetiza los aportes y emite la **Decisión Ejecutiva Final** con código y próximos pasos claros.
   - Cero tokens pagados consumidos.

5. **Persistencia Obligatoria en pgvector & GraphRAG (Regla 0):**
   - Todo aprendizaje o solución generada se persiste atómicamente en PostgreSQL 16 (`polydim_vec_db` y `polydim_active_db`).
