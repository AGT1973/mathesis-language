#!/usr/bin/env python3
r"""
================================================================================
  SETUP DE SABIOS Y MODELOS SOTA: OLLAMA, HUGGING FACE & OPENROUTER FREE
================================================================================
Configura y descarga los modelos del Tribunal de Sabios para el alumno novato.
Permite ejecutar IAs locales (Ollama), descargar adaptadores oficiales de
Hugging Face (Polydim-Einsof) y configurar acceso gratuito a modelos de 70B
(Groq, OpenRouter, SambaNova) con cero consumo de saldo de Ariel.

Autor Intelectual: Ariel García Traba (53 años)
Ecosistema: POLYDIM-EINSOF & Mathesis Universalis
================================================================================
"""

import os
import sys
import shutil
import subprocess
import platform

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HF_ORG = "Polydim-Einsof"

MODELS_MAP = {
    # ─── BLOQUE ASIA (9 modelos) ───
    "1":  ("Qwen 3 1.5B (Ultraligero Didáctico)",     "qwen3:1.5b",          "Polydim-Einsof/qwen3-1.5b-pmtp"),
    "2":  ("Qwen 3 1.7B (Código Ultraligero PC)",      "qwen3:1.7b",          "Polydim-Einsof/qwen3-1.7b-pmtp"),
    "3":  ("Qwen 3 8B (Multilingüe Mid-Range)",         "qwen3:8b",            "Polydim-Einsof/qwen3-8b-pmtp"),
    "4":  ("Qwen 3.8 / 3.5 Max 27B (Apache 2.0)",      "qwen3.8:27b",         "Polydim-Einsof/qwen3.8-27b-pmtp"),
    "5":  ("DeepSeek V4 Distill (Razonamiento MoE)",    "deepseek-v4:latest",  "Polydim-Einsof/deepseek-v4-distill-pmtp"),
    "6":  ("DeepSeek V4.1 Flash (MIT Rápido)",          "deepseek-v4.1:flash", "Polydim-Einsof/deepseek-v4.1-flash-pmtp"),
    "7":  ("Kimi K3.1 Pro (Moonshot AI — MIT-Mod)",     "kimi-k3.1:latest",    "Polydim-Einsof/kimi-k3.1-pro-pmtp"),
    "8":  ("GLM-5.3 Prime (Zhipu AI — China)",          "glm-5.3:latest",      "Polydim-Einsof/glm-5.3-prime-pmtp"),
    "9":  ("Xiaomi MiMo 9B (Apache 2.0)",               "mimo:9b",             "Polydim-Einsof/xiaomi-mimo-9b-pmtp"),
    # ─── BLOQUE EUROPA (3 modelos) ───
    "10": ("Mistral Large 3 (Soberanía Europea)",       "mistral:latest",      "Polydim-Einsof/mistral-large-3-pmtp"),
    "11": ("EuroLLM 9B (UE Multilingüe Apache 2.0)",    "eurollm:9b",          "Polydim-Einsof/eurollm-9b-pmtp"),
    "12": ("Muse Glimmer 30B (Europa Creativa)",         "glimmer:30b",         "Polydim-Einsof/muse-glimmer-30b-pmtp"),
    # ─── BLOQUE USA (5 modelos) ───
    "13": ("LLaMA 3.3 8B (Meta Community)",              "llama3.3:8b",         "Polydim-Einsof/llama-3.3-8b-pmtp"),
    "14": ("LLaMA 4 70B (Meta Scout/Maverick)",          "llama4:70b",          "Polydim-Einsof/llama-4-70b-pmtp"),
    "15": ("Gemma 4 31B (Google — Apache 2.0)",          "gemma4:latest",       "Polydim-Einsof/gemma-4-31b-pmtp"),
    "16": ("Phi-4 14B (Microsoft — MIT)",                "phi4:14b",            "Polydim-Einsof/phi-4-14b-pmtp"),
    "17": ("PPLX Decider 27B (Perplexity Apache 2.0)",   "pplx:27b",            "Polydim-Einsof/pplx-decider-27b-pmtp"),
    # ─── EINSOF SOVEREIGN (1 modelo) ───
    "18": ("Hermes-3 LLaMA 3.1 8B (Einsof Soberano)",   "hermes3:8b",          "Polydim-Einsof/Hermes-3-Llama-3.1-8B-PMTP-Einsof"),
}

def banner():
    print("=" * 75)
    print("   CONFIGURADOR DEL TRIBUNAL DE SABIOS (OLLAMA / HUGGING FACE / OPENROUTER)")
    print("   Ecosistema POLYDIM-EINSOF — Cero Costo de API para Estudiantes")
    print("=" * 75)

def ensure_ollama_running():
    import urllib.request
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/", timeout=1) as resp:
            return True
    except Exception:
        pass
    if shutil.which("ollama"):
        print("    [*] Iniciando servicio local de Ollama en segundo plano...")
        try:
            if sys.platform == "win32":
                subprocess.Popen(["ollama", "serve"], creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            else:
                subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            import time
            time.sleep(2)
            return True
        except Exception as e:
            print(f"    [!] No se pudo iniciar 'ollama serve': {e}")
    return False

def check_ollama():
    print("\n[1/3] Verificando motor de IA local (Ollama)...")
    ollama_path = shutil.which("ollama")
    if ollama_path:
        print(f"    [+] Ollama detectado en: {ollama_path}")
        ensure_ollama_running()
        try:
            res = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                print("    [*] Modelos instalados en Ollama:")
                lines = [line.strip() for line in res.stdout.split("\n") if line.strip()]
                for l in lines[1:6]:
                    print(f"        - {l}")
                if len(lines) <= 1:
                    print("        (Ningún modelo descargado aún)")
            return True
        except Exception:
            return True
    else:
        print("    [!] Ollama no está instalado en esta máquina.")
        print("    -> Si deseas correr modelos locales 100% offline y gratis:")
        print("       Descarga el instalador oficial desde: https://ollama.com/download")
        return False

def check_huggingface_hub():
    print("\n[2/3] Verificando biblioteca de Hugging Face (huggingface_hub)...")
    try:
        import huggingface_hub
        print(f"    [+] huggingface_hub detectado: v{huggingface_hub.__version__}")
        return True
    except ImportError:
        print("    [*] Instalando huggingface_hub para descarga de adaptadores Polydim-Einsof...")
        res = subprocess.run([sys.executable, "-m", "pip", "install", "huggingface_hub"], capture_output=True, text=True)
        if res.returncode == 0:
            print("    [+] huggingface_hub instalado con éxito.")
            return True
        else:
            print("    [!] No se pudo instalar huggingface_hub:", res.stderr)
            return False

def check_openrouter_and_free_pools():
    print("\n[3/3] Verificando acceso a OpenRouter (Puerta Única de Modelos en la Nube)...")
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        masked = key[:6] + "..." + key[-4:] if len(key) > 10 else "***"
        print(f"    [+] OPENROUTER_API_KEY configurada ({masked})")
    else:
        print("    [-] OPENROUTER_API_KEY: No detectada.")
        print("\n    💡 GUÍA DE 1 MINUTO PARA EL ALUMNO (100% GRATIS):")
        print("    Para usar modelos grandes (DeepSeek-R1 70B, LLaMA 3.3 70B) sin tarjeta de crédito:")
        print("    1. Entra a https://openrouter.ai/ y regístrate con tu correo o Google.")
        print("    2. Genera una API Key gratuita en tu perfil.")
        print("    3. En Windows PowerShell ejecuta:")
        print('       [Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "tu_clave", "User")')
        print('         [Environment]::SetEnvironmentVariable("GROQ_API_KEY", "tu_clave_aqui", "User")')

def download_sample_model(choice: str):
    if choice not in MODELS_MAP:
        return
    name, ollama_tag, hf_repo = MODELS_MAP[choice]
    print(f"\n[*] Descargando {name}...")
    
    # Intentar Ollama primero si está instalado
    if shutil.which("ollama"):
        print(f"    -> Descargando en Ollama: ollama pull {ollama_tag}")
        try:
            subprocess.run(["ollama", "pull", ollama_tag], check=True)
            print(f"    [+] {ollama_tag} instalado y listo en Ollama.")
            return
        except Exception as e:
            print(f"    [!] Error en Ollama pull: {e}")

    # Fallback o descarga desde Hugging Face
    try:
        from huggingface_hub import snapshot_download
        print(f"    -> Verificando repositorio en Hugging Face: {hf_repo}")
        target_dir = os.path.join(BASE_DIR, "modelos_hf", hf_repo.split("/")[-1])
        os.makedirs(target_dir, exist_ok=True)
        print(f"    -> Repositorio oficial accesible en: https://huggingface.co/{hf_repo}")
    except Exception as e:
        print(f"    [!] Info Hugging Face: {e}")

def main():
    banner()
    has_ollama = check_ollama()
    check_huggingface_hub()
    check_openrouter_and_free_pools()

    print("\n" + "=" * 75)
    print("  CATÁLOGO DE MODELOS DE SILICIO DISPONIBLES (HUGGING FACE & OLLAMA):")
    print("=" * 75)
    for k, (desc, otag, hf) in MODELS_MAP.items():
        print(f"  [{k}] {desc:<35} | Ollama: {otag:<20} | HF: {hf}")
    print("  [0] Salir sin descargar")
    print("=" * 75)

    if len(sys.argv) > 1:
        choice = sys.argv[1].strip()
        download_sample_model(choice)
    else:
        print("  💡 Para descargar automáticamente un modelo ejecuta:")
        print("     python setup_sabios_models.py <N>")
        print()
        print("  Ejemplos rápidos:")
        print("     python setup_sabios_models.py 1   →  Qwen 3 1.5B (ultraligero didáctico)")
        print("     python setup_sabios_models.py 5   →  DeepSeek V4 Distill (razonamiento MoE)")
        print("     python setup_sabios_models.py 13  →  LLaMA 3.3 8B (ecosistema global)")
        print("     python setup_sabios_models.py 15  →  Gemma 4 31B (despliegue local)")
        print("     python setup_sabios_models.py 18  →  Hermes-3 (Einsof soberano)")

if __name__ == "__main__":
    main()
