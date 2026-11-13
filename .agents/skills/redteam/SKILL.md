---
name: redteam
description: >
  Auditoría adversarial exhaustiva y simétrica (Red Team vs Blue Team).
  Busca errores, cuellos de botella, brechas de datos y bugs con máxima severidad.
  Entrega informe OBLIGATORIO con dos secciones: VULNERABILIDADES ENCONTRADAS y
  COMPONENTES QUE RESISTIERON EL ATAQUE. Certificación simétrica Anti-Cynical.
  Invocable con la acción /redteam <objetivo>.
---

# /redteam — Auditoría Adversarial Simétrica Exhaustiva

## Propósito

Ejecutar una auditoría de seguridad, rendimiento y corrección de grado profesional
sobre el componente, kernel, protocolo, arquitectura o sistema indicado por Ariel.

**NO es una búsqueda selectiva de fallos.** Es una evaluación completa que certifica
con idéntico rigor lo que FALLÓ y lo que RESISTIÓ.

---

## Doctrina Inviolable: Certificación Simétrica (Anti-Cynical Red Team)

> Un equipo Red Team contratado que busca fallas y no las encuentra NO se queda callado.
> Reporta explícitamente: "Ataqué los vectores X, Y, Z. Los vectores X e Y resistieron.
> El vector Z presentó vulnerabilidad de severidad Alta."

### Prohibiciones Absolutas:

1. **PROHIBIDO reportar solo fallos** y omitir componentes que funcionan correctamente.
   Eso es falacia por omisión, equivalente a mentir.

2. **PROHIBIDO desestimar un componente funcional con argumentos de paja.**
   Ejemplo vetado: "Ghost Protocol no sirve porque no es telepatía real."
   Realidad: Ghost Protocol ahorra >98% de tokens vs serialización 1D plana.
   El nombre es metafórico. La métrica empírica de ahorro es REAL y verificable.

3. **PROHIBIDO halagar o inflar logros sin evidencia empírica.**
   Si algo funciona, se certifica con datos (Exit Code 0, latencia, ahorro medido).
   No con adjetivos ("excelente", "brillante", "revolucionario").

4. **PROHIBIDO emitir juicios cualitativos sin script generador y log crudo.**
   Todo resultado (positivo o negativo) debe tener evidencia reproducible.

---

## Protocolo de Ejecución

### Paso 1: Recepción del Objetivo
Ariel escribe: `/redteam <componente o sistema a auditar>`

Gandalf identifica:
- Qué se va a auditar (kernel, protocolo, API, arquitectura, script, teorema)
- Superficie de ataque aplicable
- Métricas de éxito/fallo relevantes

### Paso 2: Definición de Vectores de Ataque

Construir matriz de ataque según la naturaleza del objetivo:

#### Vectores Numéricos (kernels, tensores, álgebra):
- NaN, ±Inf, ±0, subnormales IEEE-754
- Épsilon de máquina y overflow/underflow
- Vectores nulos, matrices rank-deficient
- Dimensiones asintóticas: D ≥ 10⁶
- Deriva numérica acumulada (Neumaier vs naive)

#### Vectores de Concurrencia y Memoria:
- Race conditions en slabs compartidos (PmtpShmBus)
- Doble escritura simultánea, dead locks
- Leaks en FFI boundaries (Dart↔C++, Python↔Rust)
- Slabs huérfanos sin lease activo
- RAM ≥ 80% del sistema (AMD A4-6300, 16GB DDR3)

#### Vectores de Seguridad y Datos:
- Brechas de datos en credenciales (API keys expuestas)
- Inyección SQL en queries a PostgreSQL 16
- Archivos sensibles en staging de git
- Tokens/secrets en logs o artefactos públicos

#### Vectores de Arquitectura y Diseño:
- Single points of failure
- Cuellos de botella de I/O (HDD mecánico)
- Dependencias circulares
- Acoplamiento excesivo entre componentes
- Happy-path exclusivo (sin manejo de errores)

#### Vectores de Rendimiento:
- Latencia bajo carga
- Escalabilidad vs dimensionalidad
- Consumo de tokens (gusano 1D vs Ghost Protocol)
- Tiempo de compilación y tamaño de binarios

### Paso 3: Ejecución en Silicio

- Escribir scripts de ataque concretos (Python, C++, Rust, shell)
- Ejecutar cada ataque en terminal real
- Capturar log crudo con Exit Code
- NO opinar sin haber ejecutado

### Paso 4: Generación del Informe Simétrico

El informe es un artefacto Markdown con estructura OBLIGATORIA:

```markdown
# 🔴🔵 Informe Red Team — [Nombre del Objetivo]
**Fecha:** <timestamp>
**Auditor:** Gandalf (Red Team Adversarial)
**Objetivo:** <descripción del componente auditado>

---

## 🔴 SECCIÓN ROJA: Vulnerabilidades y Fallos Encontrados

### [CRÍTICO] <Título del hallazgo>
- **Vector de ataque:** <descripción>
- **Input destructivo:** <datos exactos>
- **Resultado observado:** <log crudo>
- **Exit Code:** <código>
- **Impacto:** <qué se rompe>
- **Remediación propuesta:** <3 opciones mínimo>

### [ALTO] <Título>
...

### [MEDIO] <Título>
...

### [BAJO] <Título>
...

---

## 🔵 SECCIÓN AZUL: Componentes que Resistieron el Ataque

### ✅ <Componente que resistió>
- **Vector de ataque aplicado:** <qué se intentó>
- **Resultado observado:** <log crudo que demuestra resistencia>
- **Exit Code:** 0
- **Métrica empírica:** <dato cuantitativo verificable>
- **Certificación:** Este componente resistió el ataque adversarial
  con evidencia empírica verificable.

### ✅ <Otro componente que resistió>
...

---

## 📊 RESUMEN EJECUTIVO

| Categoría | Crítico | Alto | Medio | Bajo | Resistió |
|-----------|---------|------|-------|------|----------|
| Numérico  |    X    |  X   |   X   |  X   |    X     |
| Concurrencia | X   |  X   |   X   |  X   |    X     |
| Seguridad |    X    |  X   |   X   |  X   |    X     |
| Rendimiento |  X    |  X   |   X   |  X   |    X     |

**Veredicto global:** <APROBADO CON OBSERVACIONES / REPROBADO / APROBADO>

---

## 🔧 PLAN DE REMEDIACIÓN PRIORIZADO
1. [CRÍTICO] ...
2. [ALTO] ...
3. [MEDIO] ...
```

### Paso 5: Persistencia

- Artefacto guardado en `E:\POLYDIM_EINSOF\ENTREGA_<DATE>_REDTEAM\`
- Persistencia atómica en PostgreSQL 16:
  - `polydim_active_db.active_vault`: Estado del último Red Team
  - `polydim_vec_db.session_context`: Checkpoint con hallazgos
  - `polydim_vec_db.facts`: Cada hallazgo como fact certificado

### Paso 6: Convocatoria a Sabios (Opcional)

Si Ariel lo solicita o si los hallazgos son ambiguos:
- Enviar el informe a los Sabios (vía `/sabios` o `/profundo`)
- Cada IA ataca desde su perspectiva
- Consolidación final con certificación simétrica

---

## Ejemplo Concreto: Ghost Protocol

**Ataque cynical incorrecto (VETADO):**
> "Ghost Protocol no sirve porque no hace telepatía de verdad."

**Informe Red Team correcto:**

🔴 **Vulnerabilidades encontradas:**
- [MEDIO] El nombre "telepatía" puede generar expectativas incorrectas
  en audiencias no técnicas.
- [BAJO] La documentación no cuantifica explícitamente el ahorro de tokens
  vs serialización 1D en cada caso de uso.

🔵 **Componentes que resistieron:**
- ✅ **Ahorro de tokens:** Ghost Protocol elimina >98% del tráfico de texto
  plano en intercambios tensoriales D≥100, reemplazándolo por punteros SLAB_ID.
  Evidencia: PmtpShmBus 43.2x vs JSON serialization, 0 tokens inter-proceso,
  Exit Code 0.
- ✅ **Integridad numérica:** Neumaier norm error 0.00×10⁰ en S^{4095}.
  Stiefel defect 4.45×10⁻¹⁵ en St(256,64). Verificado en silicio.
- ✅ **Metáfora funcional:** "Telepatía" describe correctamente la transferencia
  de estados latentes sin serialización 1D intermedia, que es exactamente
  lo que hace PmtpShmBus.

---

## Reglas de Invocación

- **Trigger:** Ariel escribe `/redteam <objetivo>`
- **Autonomía:** Gandalf ejecuta el protocolo completo sin pedir permiso
- **Informe obligatorio:** Siempre con ambas secciones (Roja y Azul)
- **Evidencia obligatoria:** Exit Code 0 o log de fallo real
- **Cero opinión sin ejecución:** Si no se ejecutó, no se opina
