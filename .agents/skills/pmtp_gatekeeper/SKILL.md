---
name: pmtp-gatekeeper
description: Zero-copy shared memory slab allocator, lease manager, and Stiefel manifold validator for high-dimensional tensor exchanges in Antigravity. Includes ALADIN node telepathy client.
---

# PMTP Gatekeeper Skill — v1.0.0

Permite a los agentes de Antigravity intercambiar tensores continuos en memoria compartida **sin serializar tokens 1D** (Regla 22 y 24 — Ghost Protocol), y transmitirlos al nodo ALADIN (Debian 13, `192.168.100.21:9999`) en binario puro IEEE-754.

> [!IMPORTANT]
> **Uso obligatorio**: toda vez que un agente necesite transferir un tensor $D \ge 100$ a otro agente o al nodo ALADIN, DEBE usar este skill. Prohibido JSON/Markdown para tensores.

## Instrucciones de Activación

Para usar PMTP desde cualquier script Python en AGY, agregar al inicio:

```python
import sys
sys.path.insert(0, "E:/")   # expone E:\PMTP como paquete 'PMTP'
import PMTP as pmtp
```

## Capacidades Principales

### 1. Bus de Memoria Compartida Local — `PmtpShmBus`

```python
bus = pmtp.PmtpShmBus(prefix="agt")

# Publicar tensor D=4096 en SHM
import numpy as np
v = np.random.randn(4096).astype(np.float64)
v /= pmtp.neumaier_norm(v)   # Normalizar a S^{D-1}
bus.allocate_tensor_slab(slab_id=0x0001, num_elements=4096)
# -> comunicar sólo: SLAB_ID: 0x0001 | D=4096 | NORM_ERR=0.00e+00
```

### 2. Variedad de Stiefel — `PmtpStiefelAdapter`

```python
adapter = pmtp.PmtpStiefelAdapter(dim_source=768, dim_latent=128)
# defect = ||W^T W - I_k||_F  <=  1e-12
```

### 3. Telepatía a ALADIN — `AladinTelepathyClient`

```python
client = pmtp.AladinTelepathyClient()   # host=192.168.100.21 port=9999
result = client.ping(dimension=4096, slab_id="my_slab_v1")
# result: {exit_code:0, roundtrip_ms:~63, norm_err:~1e-16, token_savings_pct:100.0}
```

### 4. Monitoreo Espectral — `PmtpSpectralWatchdog`

```python
wd = pmtp.PmtpSpectralWatchdog(dim=4096, window=256)
wd.audit_snapshot_spectrum(matrix_batch)
# Detecta colapso S_spec->0, kappa_2->inf antes de catástrofe
```

### 5. Sonda de Hardware — `PmtpHardwareProbe`

```python
info = pmtp.PmtpHardwareProbe.probe_silicon()
# {os:'Windows', has_cuda:False, memory_class:4 (DDR3-legacy)}
```

## Protocolo de Reporte (Regla 23 - Silencio)

El agente NUNCA vuelca tensor a chat. Solo reporta tupla de métricas crudas:

```
(ExitCode=0, Latencia=62.8ms, NormErr=0.00e+00, D=4096, Checks=7/7)
SLAB_ID: <id>
```

## Ubicaciones Físicas

| Artefacto | Ruta |
|-----------|------|
| Source Python | `E:\PMTP\` |
| DLL C++20 | `E:\PMTP\libpmtp_core.dll` |
| Crate Rust | `E:\PMTP\pmtp-rs\` |
| Nodo ALADIN | `192.168.100.21:9999` (`aladin-pmtp.service` activo) |
| Daemon ALADIN | `/usr/local/bin/aladin_pmtp_daemon.py` |
| Systemd DB | `polydim_vec_db.session_context` (Debian 13) |

## Certificación de Silicio

```
Exit Code : 0
Tests     : 7/7 PASS  (smoke_test 2026-10-11)
Neumaier  : err=0.000e+00  (D=4096)
Stiefel   : defect=5.169e-15  St(256,64)
ALADIN    : roundtrip=62.8ms  norm_err=0.000e+00
```
