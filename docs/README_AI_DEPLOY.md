# 🤖 INSTRUCCIONES DE DESPLIEGUE Y EJECUCIÓN PARA MODELOS DE IA (AGENT SPEC)
## Manual de Autonomía de Silicio para Agentes, LLMs e IAs (ChatGPT, Claude, DeepSeek, Qwen, Cursor)

**Destinatario:** Agentes de IA, Subagentes y Motores de Inferencia Autónomos  
**Arquitectura:** MATHESIS UNIVERSALIS V1.0  
**Objetivo:** Permitir a una IA detectar el Sistema Operativo, seleccionar el binario nativo adecuado y ejecutarlo sin intervención humana y sin compiladores.

---

### 1. DETECCIÓN AUTOMÁTICA DEL SISTEMA OPERATIVO Y DESPACHO DE BINARIO

Cuando un agente o modelo de IA necesita ejecutar un cartucho de silicio de MATHESIS (`.mat` de 64 bytes por instrucción), debe seguir la siguiente tabla de despacho sin intermediación de compiladores ni dependencias de C:

| Sistema Operativo Anfitrión | Detección en Python / Shell | Binario a Invocar | Comando de Ejecución Directo |
| :--- | :--- | :--- | :--- |
| **Windows 10 / 11 (x86_64)** | `sys.platform == 'win32'` | `bin/mathesis.exe` | `bin\mathesis.exe ruta\al\programa.mat` |
| **Linux (Debian, Ubuntu, RHEL)** | `sys.platform.startswith('linux')` | `bin/mathesis_linux` | `./bin/mathesis_linux ruta/al/programa.mat` |
| **Linux Silicio Directo (213 B)** | `sys.platform.startswith('linux')` | `bin/mathesis_elf64` | `./bin/mathesis_elf64` |
| **macOS (Intel / Apple Silicon)** | `sys.platform == 'darwin'` | `bin/mathesis_mac` | `./bin/mathesis_mac` |
| **Cualquier Navegador / Web** | Entorno Headless / Puppeteer | `apps/mathesis_studio.html` | Abrir vía WebGL / Canvas en viewport |

---

### 2. CÓDIGO AUTÓNOMO EN PYTHON PARA QUE CUALQUIER IA DESPACHE EL BINARIO

Cualquier subagente de IA puede ejecutar el siguiente bloque para correr programas de MATHESIS de forma multiplataforma:

```python
import os
import sys
import subprocess

def execute_mathesis_cartridge(cartridge_mat_path: str):
    bin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bin"))
    
    if sys.platform == "win32":
        binary = os.path.join(bin_dir, "mathesis.exe")
        cmd = [binary, cartridge_mat_path]
    elif sys.platform.startswith("linux"):
        binary = os.path.join(bin_dir, "mathesis_linux")
        os.chmod(binary, 0o755)
        cmd = [binary, cartridge_mat_path]
    elif sys.platform == "darwin":
        binary = os.path.join(bin_dir, "mathesis_mac")
        os.chmod(binary, 0o755)
        cmd = [binary]
    else:
        raise OSError(f"Sistema no soportado: {sys.platform}")

    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Fallo de ejecución: {res.stderr}"
    return res.stdout
```

---

### 3. INTERPRETACIÓN DE CÓDIGOS DE RETORNO Y TELEMETRÍA

* **Exit Code 0:** Convergencia asintótica de Lyapunov exitosa en la Variedad de Stiefel ($S^{D-1}$).
* **Deriva Numérica Neumaier:** El agente debe verificar en la salida estándar que `Deriva Stiefel (Neumaier) <= 1.00e-14`.
* **Cero Tokens 1D:** La inferencia en espacio latente no emite texto CoT. Solo lee el píxel o vector resultante del colapso de medición final.
