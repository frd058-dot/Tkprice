import requests, json, os, time

# SİZİN BAŞARILI OLAN GOOGLE LİNKİNİZİ BURAYA YAPIŞTIRIN
GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycbzQHICP8Yldkcl5L_rwpJ6mnvA9T3XqCfMmaad2c7qmwZnM1U3lZm2Vk4i6nkirRknpBg/exec"

# Taranacak tüm ürün dosyalarınız
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
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            items = data if isinstance(data, list) else []
            if isinstance(data, dict):
                for k in data:
                    if isinstance(data[k], list): items.extend(data[k])
            
            for item in items:
                if not isinstance(item, dict): continue
                pid = item.get('id')
                name = item.get('model') or item.get('name') or item.get('title')
                
                if pid and name:
                    # İsimdeki karmaşık ekleri temizle
                    search_name = str(name).split('GHz')[0].split('Cache')[0].strip()
                    print(f"Sorgulanıyor: {search_name}")
                    
                    try:
                        res = requests.get(f"{GOOGLE_PROXY_URL}?name={requests.utils.quote(search_name)}", timeout=30)
                        if res.status_code == 200 and "Bulunamadı" not in res.text:
                            price = res.text.strip()
                            results[str(pid)] = {"price_tr": price}
                            print(f"  => OK: {price}")
                    except: pass
                    # Google'ı yormamak için kısa bekleme
                    time.sleep(0.5)
    except: continue

# Sonuçları kaydet
with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nİŞLEM TAMAM! updates.json içine {len(results)} ürün kaydedildi.")
