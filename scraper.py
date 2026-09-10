import requests, json, os, time

# SİZİN SONU /exec İLE BİTEN GOOGLE LİNKİNİZ
GOOGLE_PROXY = "https://script.google.com/macros/s/AKfycbw2UswJ223WHjWbBToYkFIHyHXdue4TX8q4mXIiyp58i0OY_zYHcR3z4y1MHYruLlMndQ/exec"

DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'rams.json', 'psus.json']
results = {}

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    print(f"\n--- {file_name} ---")
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        items = data if isinstance(data, list) else []
        for item in items:
            if not isinstance(item, dict): continue
            pid = item.get('id')
            name = (item.get('model') or item.get('name', '')).split('GHz')[0].split('Cache')[0].strip()
            
            if pid and name:
                print(f"Sorgu: {name}")
                try:
                    res = requests.get(f"{GOOGLE_PROXY}?name={requests.utils.quote(name)}", timeout=45)
                    if res.status_code == 200:
                        # Google artık bir nesne dönüyor: {price_tr, price_usd, price_eur}
                        results[pid] = res.json()
                        print(f"  [OK] TR: {results[pid]['price_tr']} | USA: {results[pid]['price_usd']}")
                except: print(f"  [Hata] {name}")
                time.sleep(0.5)

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
