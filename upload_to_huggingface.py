"""
upload_to_huggingface.py — Sincroniza y pisa los modelos canónicos certificados en Hugging Face (polydim-einsof).
Conforme a la Regla 45 y Directivas de Silicio de EinsofOS.
"""

import os
import sys
import json
from pathlib import Path
from huggingface_hub import HfApi, create_repo

HF_EXPORT_DIR = Path(r"E:\POLYDIM_EINSOF\hf_export")
ORG_NAME = "Polydim-Einsof"

CANONICAL_MODELS = [
    "qwen3-1.7b-pmtp",
    "qwen3-8b-pmtp",
    "qwen3.8-27b-pmtp",
    "deepseek-v4-distill-pmtp",
    "llama-3.3-8b-pmtp",
    "llama-4-70b-pmtp",
    "muse-glimmer-30b-pmtp",
    "Hermes-3-Llama-3.1-8B-PMTP-Einsof",
    "phi-4-14b-pmtp",
    "pplx-decider-27b-pmtp",
    "xiaomi-mimo-9b-pmtp"
]

def main():
    token = os.environ.get("HF_TOKEN")
    if not token and len(sys.argv) > 1:
        token = sys.argv[1].strip()

    if not token:
        try:
            import psycopg2
            conn = psycopg2.connect("dbname=polydim_active_db user=postgres host=localhost port=5432")
            cur = conn.cursor()
            cur.execute("SELECT value FROM active_vault WHERE key_name = 'HuggingFace_Polydim_Einsof' ORDER BY updated_at DESC LIMIT 1;")
            row = cur.fetchone()
            conn.close()
            if row and row[0] and row[0].startswith("hf_"):
                token = row[0].strip()
        except Exception:
            pass

    if not token:
        print("[ERROR] No se detecto HF_TOKEN en el entorno, argumentos ni en active_vault.")
        print("Uso: python upload_to_huggingface.py <TU_HF_TOKEN_DE_ESCRITURA>")
        sys.exit(1)

    api = HfApi(token=token)
    try:
        user_info = api.whoami()
        print(f"[AUTH OK] Autenticado en Hugging Face como: {user_info.get('name')}")
    except Exception as e:
        print(f"[AUTH ERROR] Token invalido o sin conexion: {e}")
        sys.exit(1)

    print("=" * 70)
    print(f"SINCRONIZANDO Y PISANDO MODELOS EN HUGGING FACE ({ORG_NAME})")
    print("=" * 70)

    success_count = 0
    for model_dir_name in CANONICAL_MODELS:
        local_folder = HF_EXPORT_DIR / model_dir_name
        if not local_folder.exists():
            print(f"[SKIP] Carpeta local no encontrada: {local_folder}")
            continue

        repo_id = f"{ORG_NAME}/{model_dir_name}"
        print(f"\n[*] Procesando {repo_id} desde {local_folder}...")

        try:
            # Crear repo si no existe
            api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True, private=False)
            
            # Subir y pisar archivos
            future = api.upload_folder(
                folder_path=str(local_folder),
                repo_id=repo_id,
                repo_type="model",
                commit_message="feat(stiefel): actualizar pesos y configuracion formal V_TURING_013 (1736 teoremas, Stiefel <= 1e-15)"
            )
            print(f"[UPLOAD OK] {repo_id} actualizado con exito.")
            success_count += 1
        except Exception as e:
            print(f"[UPLOAD FAIL] Error en {repo_id}: {e}")

    print("\n" + "=" * 70)
    print(f"RESUMEN: {success_count}/{len(CANONICAL_MODELS)} modelos subidos a https://huggingface.co/{ORG_NAME}")
    print("=" * 70)

if __name__ == "__main__":
    main()
