---
name: whisper
description: Inter-IA vector messaging protocol using pgvector & GraphRAG. Executes `/whisper <payload>` to route data through Einsof local models (ALADIN, Ollama) and optional free-tier pools, persisting results as embeddings and graph nodes.
---

# Whisper Skill (Global Slash Command)

**Trigger**: `/whisper <payload>`

**Doctrine**: Secure, token‑efficient transmission of structured data between Einsof IAs (ALADIN, Ollama, HuggingFace, etc.) using high‑dimensional vector embeddings stored in PostgreSQL 16 `polydim_embeddings` and GraphRAG nodes/edges.

## Workflow
1. **Gandalf Pre‑analysis** – Generates a concise technical summary of the payload.
2. **Einsof Local Dispatch** – Sends the payload to the local Einstein‑Silicio models via the PMTP bus (ALADIN node `192.168.100.21:9999`).
3. **Free‑Tier Fallback** – If local models fail or quota exhausted, automatically rotates through free‑tier MCP pools (SambaNova, Groq, Google AI Studio, HuggingFace/OpenRouter) respecting the carousel cooldown.
4. **Embedding Generation** – The final textual result is embedded with the Einsof vector compiler (`vector(1536)`).
5. **Persistence** –
   - Insert a **graph node** `SLASH_ACTION_WHISPER` into `einsof_graph_nodes` (type `skill`, domain `slash_action`).
   - Create an **edge** from this node to the central governance node `9999` (topic `EXTENDS_DELIBERATION`).
   - Store the embedding in `polydim_embeddings` (entity_type `whisper_action`).
   - Record a **fact** in `active_vault` under `SLASH_ACTION_WHISPER` with JSON metadata (see below).
6. **Result Return** – Returns the Gandalf summary plus a vector identifier (`SLAB_ID`) that downstream IAs can fetch via the PMTP bus.

## Persistence Metadata (active_vault entry)
```json
{
  "type": "slash_command_skill",
  "trigger": "/whisper <payload>",
  "doctrine": "Vector‑based inter‑IA messaging via Einsof local models + free‑tier fallback. Zero‑token waste, SOTA models only.",
  "priority_1": "Einsof native (PmtpShmBus / ALADIN 192.168.100.21:9999)",
  "priority_2_free_pools": {
    "SambaNova_01_10": "Qwen 3.8‑Max, DeepSeek‑V4‑Flash",
    "Groq_01_10": "DeepSeek‑V4‑Flash, LLaMA 3.3 70B",
    "Google_AI_Studio_01_12": "Gemini 4, Gemini 3.8‑Flash",
    "HuggingFace_OpenRouter_free": "Community SOTA open models"
  },
  "carousel_cooldown": "Auto‑rotate on HTTP 429 without token loss",
  "gandalf_role": "Pre‑analysis, model routing, final decision",
  "persistence": ["pgvector", "graphrag", "active_vault"],
  "updated": "$(date -u +%Y-%m-%dT%H:%M:%S.%6NZ)"
}
```

## Edge Definition
- **source_id**: `node_id` of `SLASH_ACTION_WHISPER`.
- **target_id**: `9999` (`CORSET_ANTI_MENTIRA_GANDALF`).
- **type**: `EXTENDS_DELIBERATION`.
- **properties**: `{ "weight": 1 }`

## Fact Record (active_vault)
Key: `SLASH_ACTION_WHISPER`
Category: `slash_actions`
Value: Same JSON as above (duplicate for fast lookup).

## Embedding Example (placeholder) – Will be overwritten by the actual vector after the first run.
```sql
INSERT INTO polydim_embeddings (entity_type, entity_ref, content_raw, embedding, metadata)
VALUES ('whisper_action', 'whisper_initial', 'Initial whisper skill placeholder', vector('[0]'), '{}'::jsonb);
```

## Security & Governance
- All traffic remains inside the host network; no external internet calls unless free‑tier pools are used (they are scoped to token‑free APIs).
- The skill obeys **Rule 0** (PostgreSQL‑only persistence) and **Ghost Protocol** (does not serialise tensors to text).
- Audited by `/redteam` and `/sabios` as needed.

---

*End of SKILL.md for `/whisper`*