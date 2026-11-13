"""
gandalf_sync_on_boot.py — Sincronizador Pull Soberano (Workstation / Gandalf)
Descarga resultados pendientes acumulados en download_queue de ALADIN (192.168.100.21)
cuando el workstation arranca. Exit Code 0 garantizado.
"""

import sys
import os
import json
import subprocess
import psycopg2

ALADIN_HOST = "192.168.100.21"
LOCAL_DB = "dbname=polydim_active_db user=postgres password=polydim_einsof host=localhost port=5432"

def fetch_aladin_pending():
    """Consulta download_queue en ALADIN vía SSH + Python local de ALADIN."""
    remote_script = """
import psycopg2, json

conn = psycopg2.connect(dbname='polydim_active_db', user='postgres', password='postgres', host='127.0.0.1', port=5432)
cur = conn.cursor()
cur.execute("SELECT id, category, key_name, payload, created_at FROM download_queue WHERE status='PENDING' ORDER BY id ASC;")
rows = cur.fetchall()
res = []
for r in rows:
    res.append({
        'id': r[0],
        'category': r[1],
        'key_name': r[2],
        'payload': r[3],
        'created_at': str(r[4])
    })
print('JSON_DATA:' + json.dumps(res))
conn.close()
"""
    p = subprocess.run(["ssh", f"root@{ALADIN_HOST}", "python3"], input=remote_script, capture_output=True, text=True, timeout=15)
    if p.returncode != 0:
        print(f"[!] Error SSH a ALADIN: {p.stderr}")
        return []
    
    for line in p.stdout.splitlines():
        if line.startswith("JSON_DATA:"):
            return json.loads(line[len("JSON_DATA:"):])
    return []

def mark_aladin_delivered(item_ids):
    if not item_ids:
        return
    remote_script = f"""
import psycopg2

conn = psycopg2.connect(dbname='polydim_active_db', user='postgres', password='postgres', host='127.0.0.1', port=5432)
cur = conn.cursor()
cur.execute('''
    UPDATE download_queue
    SET status='DELIVERED', delivered_at=NOW(), delivered_to='NODE1_WORKSTATION'
    WHERE id = ANY(%s);
''', ({item_ids},))
conn.commit()
conn.close()
print('DELIVERED_OK')
"""
    p = subprocess.run(["ssh", f"root@{ALADIN_HOST}", "python3"], input=remote_script, capture_output=True, text=True, timeout=15)
    return p.returncode == 0

def sync_to_local_vault():
    print(f"[*] Iniciando sincronización Pull desde ALADIN ({ALADIN_HOST})...")
    items = fetch_aladin_pending()
    if not items:
        print("[+] Cola download_queue en ALADIN está vacía. Cero pendientes.")
        return 0

    print(f"[+] Descargando {len(items)} paquetes pendientes de ALADIN...")
    conn_loc = psycopg2.connect(LOCAL_DB)
    cur_loc = conn_loc.cursor()

    delivered_ids = []
    for item in items:
        k_id = item['id']
        cat = item['category']
        key_name = item['key_name']
        payload = item['payload']

        cur_loc.execute("""
            INSERT INTO active_vault (category, key_name, value, updated_at)
            VALUES (%s, %s, %s, NOW())
            ON CONFLICT (category, key_name) DO UPDATE
            SET value = EXCLUDED.value, updated_at = NOW();
        """, (cat, key_name, json.dumps(payload)))
        delivered_ids.append(k_id)
        print(f"    -> Integrado en active_vault: [{cat}] {key_name}")

    conn_loc.commit()
    conn_loc.close()

    # Marcar entregados en ALADIN
    if mark_aladin_delivered(delivered_ids):
        print(f"[+] {len(delivered_ids)} elementos marcados como DELIVERED en ALADIN.")
    else:
        print(f"[!] Advertencia: No se pudo actualizar el flag DELIVERED en ALADIN.")

    return len(delivered_ids)

if __name__ == "__main__":
    count = sync_to_local_vault()
    
    # Sincronización oportunista de POLYDIM SUITE (Regla 20) al encendido del Workstation
    try:
        suite_script = r"E:\SUITE\sync_suite_watchdog.py"
        if os.path.exists(suite_script):
            subprocess.run([sys.executable, suite_script], check=False, timeout=60)
    except Exception as e:
        print(f"[!] Advertencia al ejecutar sync_suite_watchdog: {e}")
        
    sys.exit(0)
