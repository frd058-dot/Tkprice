import requests, json, os, time

GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycbxWppt-80fiTCRyk-2xbORlmSBF-huZKhc8jpZMfR1VAblwwJw2Dw5lOE7aUw-owUbfVA/exec"

DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'rams.json', 'storages.json']
results = {}

def get_simple_name(name):
    """Sadece ilk 2 kelimeyi alır (Örn: Intel Core i5 -> Intel Core)"""
    words = str(name).replace("-", " ").split()
    return " ".join(words[:2]).strip()

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    print(f"\n--- {file_name} ---")
    with open(file_name, 'r', encoding='utf-8') as f:
        try:
            items = json.load(f)
            if isinstance(items, dict):
                for k in items:
                    if isinstance(items[k], list): items = items[k]; break
            
            for item in items:
                if not isinstance(item, dict): continue
                pid = item.get('id')
                name = item.get('model') or item.get('name')
                
                if pid and name:
                    search_name = get_simple_name(name)
                    print(f"Aranıyor: {search_name}")
                    try:
                        res = requests.get(f"{GOOGLE_PROXY_URL}?name={requests.utils.quote(search_name)}", timeout=30)
                        if "Bulunamadı" not in res.text and "Hata" not in res.text:
                            results[pid] = {"price_tr": res.text.strip()}
                            print(f"  => OK: {res.text}")
                        else:
                            print(f"  => Yok")
                    except: pass
                    time.sleep(1) # Hızlanmak için bekleme düştü
        except: continue

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
