import requests, json, os, time

GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycbybST-0ZsYhlodNx_zVCZLspY_nuQluNbpD53SDoMT-cHI50Pn3t5kVaXim4rtxP9gwrA/exec"

DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'rams.json', 'psus.json', 'monitors.json']
results = {}

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    print(f"\n--- {file_name} ---")
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            items = data if isinstance(data, list) else []
            if isinstance(data, dict):
                for k in data:
                    if isinstance(data[k], list): items = data[k]; break
            
            for item in items:
                if not isinstance(item, dict): continue
                pid = item.get('id')
                brand = str(item.get('brand', '')).strip()
                model = str(item.get('model') or item.get('name', '')).strip()
                
                if pid and model:
                    # Akakçe için ideal arama ismi oluştur (Marka + Model)
                    search_name = model if brand.lower() in model.lower() else f"{brand} {model}"
                    # "GHz", "Cache" gibi teknik detayları sil ama "RTX 4060" gibi ana modeli koru
                    search_name = search_name.split('GHz')[0].split('Cache')[0].strip()
                    
                    print(f"Akakce Sorgusu: {search_name}")
                    try:
                        res = requests.get(f"{GOOGLE_PROXY_URL}?name={requests.utils.quote(search_name)}", timeout=30)
                        if "Bulunamadı" not in res.text and "Hata" not in res.text:
                            results[pid] = {"price_tr": res.text.strip()}
                            print(f"  => OK: {res.text}")
                        else:
                            print(f"  => Bulunamadı")
                    except: pass
                    time.sleep(1) # Akakçe'den banlanmamak için
    except Exception as e:
        print(f"Dosya hatası: {e}")

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nISLEM BITTI! Akakce uzerinden {len(results)} fiyat cekildi.")
