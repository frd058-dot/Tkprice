import requests, json, os, time

# 1. Adımdaki YENİ Google Script URL'nizi buraya yapıştırın
GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycbzoOtNWGUUt63qqvKtGM_YNW1OTAhR-novAdJI3xglkuxtfO5oahXOvfh5vEshx046dFw/exec"

DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'hdds.json', 'imacs.json', 'mac_minis.json', 'monitors.json', 'notebook_configs.json', 'psus.json', 'rams.json', 'sata_ssds.json', 'storages.json', 'macbooks.json']
results = {}

print(f"Mevcut dosyalar: {os.listdir('.')}")

for file_name in DATA_FILES:
    if not os.path.exists(file_name):
        print(f"Dosya bulunamadı, atlanıyor: {file_name}")
        continue
    
    print(f"\n--- {file_name} İşleniyor ---")
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Veri listeyse doğrudan al, sözlükse içindeki listeleri bul
            items = []
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                for k in data:
                    if isinstance(data[k], list):
                        items.extend(data[k])
            
            for item in items:
                # ÇÖZÜM: Sadece ürün kutusu (sözlük) olanları işle, düz metinleri atla
                if not isinstance(item, dict):
                    continue
                
                pid = item.get('id')
                name = item.get('model') or item.get('name') or item.get('title')
                
                if pid and name:
                    try:
                        # Google Proxy üzerinden sorgula
                        res = requests.get(f"{GOOGLE_PROXY_URL}?name={requests.utils.quote(str(name))}", timeout=20)
                        if res.status_code == 200 and "Bulunamadı" not in res.text and "Hata" not in res.text:
                            price_val = res.text.strip()
                            results[str(pid)] = {"price_tr": price_val}
                            print(f"  OK: {name} -> {price_val}")
                    except:
                        print(f"  Sorgu Hatası: {name}")
                    
                    time.sleep(0.5)
    except Exception as e:
        print(f"Dosya okuma hatası ({file_name}): {e}")

# updates.json dosyasını kaydet
with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nİşlem bitti! updates.json içine {len(results)} ürün kaydedildi.")
