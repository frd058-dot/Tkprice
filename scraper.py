import requests, json, os, time

GOOGLE_PROXY = "https://script.google.com/macros/s/AKfycbw2UswJ223WHjWbBToYkFIHyHXdue4TX8q4mXIiyp58i0OY_zYHcR3z4y1MHYruLlMndQ/exec"

DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'rams.json', 'psus.json', 'storages.json', 'monitors.json']
results = {}

def is_price_valid(price_str):
    """Sadece taksit miktarını eleyen basit kontrol"""
    try:
        val = int("".join(filter(str.isdigit, price_str.split(',')[0])))
        # Eğer bir parça fiyatı 1.000 TL'den düşükse muhtemelen taksittir, alma.
        return val > 1000
    except: return False

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    print(f"\n--- {file_name} İşleniyor ---")
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        items = data if isinstance(data, list) else []
        for item in items:
            pid, name = item.get('id'), (item.get('model') or item.get('name', ''))
            if pid and name:
                print(f"Sorgu: {name}")
                try:
                    res = requests.get(f"{GOOGLE_PROXY}?name={requests.utils.quote(name)}", timeout=50)
                    if res.status_code == 200:
                        p = res.json()
                        if p.get('price_tr') and is_price_valid(p['price_tr']):
                            results[pid] = p
                            print(f"  [TAMAM] {p['price_tr']}")
                        else:
                            print(f"  [RED] Hatalı/Taksit: {p.get('price_tr')}")
                except: pass
                time.sleep(1)

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
