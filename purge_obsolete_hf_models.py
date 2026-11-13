"""
purge_obsolete_hf_models.py — Purga controlada de modelos obsoletos en Hugging Face (Polydim-Einsof).
Conforme a la Regla 6 (SOTA Model Enforcement) y Regla 1 (Radical Honesty).
"""

import sys
import os
import psycopg2
from huggingface_hub import HfApi

OBSOLETE_MODELS = [
    # Qwen 2.5 (Vetado por Regla 6 -> Qwen 3)
    "Polydim-Einsof/qwen2.5_coder_0.5b_PMTP_polydim_einsof",
    "Polydim-Einsof/qwen2.5_coder_1.5b_PMTP_polydim_einsof",
    "Polydim-Einsof/Qwen2.5-Coder-32B-Einsof-LoRA",
    "Polydim-Einsof/Qwen2.5-72B-Instruct-Einsof-LoRA",
    
    # DeepSeek R1 / V3 legacy (Vetado por Regla 6 -> DeepSeek V4)
    "Polydim-Einsof/deepseek_r1_1.5b_PMTP_polydim_einsof",
    "Polydim-Einsof/deepseek_r1_7b_PMTP_polydim_einsof",
    "Polydim-Einsof/DeepSeek-R1-Distill-Qwen-14B-Einsof-LoRA",
    
    # LLaMA 3.1 / 3.2 (Superados por LLaMA 3.3 / 4)
    "Polydim-Einsof/llama3.2_3b_PMTP_polydim_einsof",
    "Polydim-Einsof/llama3.1_8b_PMTP_polydim_einsof",
    
    # Gemma 2 (Superado por Gemma 3)
    "Polydim-Einsof/gemma2_2b_PMTP_polydim_einsof",
    "Polydim-Einsof/gemma2_9b_PMTP_polydim_einsof",
    
    # GLM 4 (Superado por GLM 5.3)
    "Polydim-Einsof/glm4_9b_PMTP_polydim_einsof",
    
    # Kimi k1.5 (Superado por Kimi k3)
    "Polydim-Einsof/Kimi-k1.5-LongContext-Einsof-LoRA",
]

def get_token():
    # 1. Argumento CLI
    if len(sys.argv) > 1 and sys.argv[1].startswith("hf_"):
        return sys.argv[1].strip()
        
    # 2. Variable de entorno
    env_tok = os.environ.get("HF_TOKEN")
    if env_tok and env_tok.startswith("hf_"):
        return env_tok.strip()
        
    # 3. active_vault PostgreSQL 16
    try:
        conn = psycopg2.connect("dbname=polydim_active_db user=postgres host=localhost port=5432")
        cur = conn.cursor()
        cur.execute("SELECT value FROM active_vault WHERE key_name = 'HuggingFace_Polydim_Einsof' ORDER BY updated_at DESC LIMIT 1;")
        row = cur.fetchone()
        conn.close()
        if row and row[0] and row[0].startswith("hf_"):
            return row[0].strip()
    except Exception:
        pass
        
    return None

def main():
    token = get_token()
    if not token:
        print("[!] ERROR: No se detectó un token válido de Hugging Face.")
        print("    Uso: python purge_obsolete_hf_models.py hf_TU_TOKEN_WRITE")
        sys.exit(1)
        
    api = HfApi(token=token)
    try:
        who = api.whoami()
        print(f"[+] Autenticado en HF como: {who.get('name')}")
    except Exception as e:
        print(f"[!] Error de autenticación: {e}")
        sys.exit(1)
        
    print("=" * 75)
    print(f"  PURGANDO {len(OBSOLETE_MODELS)} REPOSITORIOS OBSOLETOS EN HUGGING FACE")
    print("=" * 75)
    
    purged = 0
    errors = 0
    
    for repo_id in OBSOLETE_MODELS:
        try:
            print(f"[*] Eliminando: {repo_id}...")
            api.delete_repo(repo_id=repo_id, repo_type="model")
            print(f"    [+] PURGADO EXITOSAMENTE.")
            purged += 1
        except Exception as e:
            err = str(e)
            if "404" in err or "Repository not found" in err:
                print(f"    [-] Ya no existe (404 Not Found).")
                purged += 1
            else:
                print(f"    [!] Error al eliminar: {err[:100]}")
                errors += 1
                
    print("=" * 75)
    print(f"[+] RESUMEN: {purged} repositorios purgados | {errors} errores")
    print("=" * 75)

if __name__ == "__main__":
    main()
