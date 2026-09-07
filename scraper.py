import requests, json, os, time

# 1. Adımdaki YENİ Google Script URL'sini buraya yapıştırın
GOOGLE_PROXY_URL = "BURAYA_YENI_GOOGLE_LINKINI_YAPISTIRIN"

DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'hdds.json', 'imacs.json', 'mac_minis.json', 'monitors.json', 'notebook_configs.json', 'psus.json', 'rams.json', 'sata_ssds.json', 'storages.json', 'macbooks.json']
results = {}

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    with open(file_name, 'r', encoding='utf-8') as f:
        items = json.load(f)
        if isinstance(items, dict): # Format kontrolü
            for k in items:
                if isinstance(items[k], list): items = items[k]; break
        for item in items:
            pid, name = item.get('id'), (item.get('model') or item.get('name'))
            if pid and name:
                try:
                    res = requests.get(f"{GOOGLE_PROXY_URL}?name={name}", timeout=20)
                    if res.status_code == 200 and "Bulunamadı" not in res.text:
                        results[pid] = {"price_tr": res.text.strip()}
                        print(f"BULDUM: {name} -> {res.text}")
                except: pass
                time.sleep(0.5)

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
