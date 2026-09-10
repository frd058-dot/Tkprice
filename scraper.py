import requests, json, os, time

# SİZİN GOOGLE SCRİPT LİNKİNİZ
GOOGLE_PROXY = "https://script.google.com/macros/s/AKfycbwDfPQRamV9dnyxGRd_6KmeViUjJ0ZGywoa5f7mw0rUsr5cQkQ_kzQ2QSrlCI607Hdc/exec"

DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'rams.json', 'sata_ssds.json', 'hdds.json', 'psus.json', 'monitors.json']
results = {}

def get_numeric(p_str):
    try:
        return int("".join(filter(str.isdigit, p_str.split(',')[0])))
    except: return 0

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    print(f"\n--- {file_name} ---")
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            items = data if isinstance(data, list) else []
            for item in items:
                if not isinstance(item, dict): continue
                pid = item.get('id')
                name = item.get('model') or item.get('name')
                
                if pid and name:
                    print(f"Yandex Sorgusu: {name}")
                    try:
                        res = requests.get(f"{GOOGLE_PROXY}?name={requests.utils.quote(str(name))}", timeout=45)
                        if res.status_code == 200:
                            p = res.json()
                            # YALNIZCA GERÇEK FİYATLARI KABUL ET (1000 TL ÜSTÜ)
                            if p.get('price_tr') and get_numeric(p['price_tr']) > 1000:
                                results[pid] = p
                                print(f"  [BAŞARILI] {p['price_tr']}")
                            else:
                                print(f"  [RED] Taksit veya hatalı veri elendi.")
                    except: pass
                    time.sleep(1.2) # Yandex'i yormadan güvenli geçiş
    except: continue

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nZAFER! Yandex destekli dünya fiyatları güncellendi.")
