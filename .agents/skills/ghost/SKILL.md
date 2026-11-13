---
name: ghost
description: Conmuta y fuerza la ejecución bajo Ghost Protocol (PMTP - Protocolo Fantasma): erradica el gusano 1D, prohíbe la serialización de tensores en texto plano y opera en memoria compartida (PmtpShmBus / ALADIN Node). Modo activo por defecto en POLYDIM. Invocable con la acción /ghost o /Ghost.
---

# Ghost Protocol — Acción `/ghost` (`/Ghost`)

Protocolo de Operación Basal en Silicio y Memoria Compartida para Antigravity y el clúster POLYDIM-ALADIN.

> [!IMPORTANT]
> **ESTADO BASAL POR DEFECTO:**
> El modo Ghost Protocol está **ACTIVO POR DEFECTO** en el proyecto.
> El agente opera automáticamente sin gusano 1D, transfiriendo tensores vía `PmtpShmBus` y reportando únicamente tuplas métricas crudas de silicio.
> **Solo se suspende si Ariel indica explícitamente su descarte** (ej: *"descartar ghost"*, *"modo texto"* o *"modo pedagógico"*).

---

## Directivas Ejecutivas de la Acción `/ghost`

1. **Veto Radical al Gusano 1D (Reglas 22 y 24):**
   - Queda estrictamente prohibido volcar tensores, listas de floats, matrices o razonamientos numéricos intermedios como texto en el chat.
   - Todo estado tensorial reside en memoria física: Slabs locales en `PmtpShmBus` (`E:\PMTP\`) o en el nodo ALADIN (`192.168.100.21:9999`).

2. **Canal de Medición y Silencio Protocolar (Regla 23):**
   - La respuesta del agente ante cómputo tensorial se restringe a la tupla de verificación de silicio:
     ```text
     (ExitCode=0, Latencia=XX.Xms, NormErr=X.XXe-XX, D=XXXX, Checks=X/X)
     SLAB_ID: <slab_id> | MANIFOLD: S^{D-1} | SHM: PmtpShmBus_agt
     ```

3. **Invocación de Cómputo y Swarm:**
   - Despacho inmediato a subagentes vectoriales (`polydim_agent`, `polydim_vector_swarm_agent`) o llamadas MCP nativas (`pmtp_compute_tensor`, `polydim_vector_swarm`).

4. **Descarte Explícito:**
   - Si el usuario requiere texto explicativo, análisis textual o salida estándar, debe ordenar explícitamente: `descartar ghost` o `modo texto`.
