import requests, json, os, time

# Google Script Linkinizi buraya yapıştırın
GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycbzoOtNWGUUt63qqvKtGM_YNW1OTAhR-novAdJI3xglkuxtfO5oahXOvfh5vEshx046dFw/exec"

DATA_FILES = [
    'cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 
    'cases.json', 'coolers.json', 'hdds.json', 'imacs.json', 
    'mac_minis.json', 'macbooks.json', 'monitors.json', 
    'motherboard.json', 'notebook_configs.json', 'psus.json', 
    'rams.json', 'sata_ssds.json', 'storages.json'
]

results = {}

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    print(f"\n--- {file_name} taranıyor ---")
    with open(file_name, 'r', encoding='utf-8') as f:
        try:
            items = json.load(f)
            if isinstance(items, dict):
                for k in items:
                    if isinstance(items[k], list): items = items[k]; break
            
            for item in items:
                if not isinstance(item, dict): continue
                pid = item.get('id')
                # İsim temizleme: "Intel Core i3 13100" gibi temiz isimler aransın
                name = item.get('model') or item.get('name') or item.get('title')
                
                if pid and name:
                    try:
                        # İsimden gereksiz ekleri temizle (Daha iyi arama sonucu için)
                        search_name = str(name).split('(')[0].strip()
                        res = requests.get(f"{GOOGLE_PROXY_URL}?name={requests.utils.quote(search_name)}", timeout=25)
                        
                        if res.status_code == 200 and "Bulunamadı" not in res.text:
                            price = res.text.strip()
                            results[str(pid)] = {"price_tr": price}
                            print(f"  BULDUM: {search_name} -> {price}")
                        else:
                            print(f"  Bulunamadı: {search_name}")
                    except: pass
                    time.sleep(0.3) # Google'ı yormadan hızlıca devam et
        except: continue

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nBİTTİ! updates.json içine {len(results)} ürün kaydedildi.")
