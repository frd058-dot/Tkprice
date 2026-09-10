import requests, json, os, time

# BURAYA SİZİN SONU /exec İLE BİTEN LİNKİNİZİ YAPIŞTIRIN
GOOGLE_PROXY = "https://script.google.com/macros/s/AKfycbwDfPQRamV9dnyxGRd_6KmeViUjJ0ZGywoa5f7mw0rUsr5cQkQ_kzQ2QSrlCI607Hdc/exec"

# Taranacak dosyalar
DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'rams.json', 'psus.json']
results = {}

print("Bot Başlatıldı. Google üzerinden fiyatlar çekiliyor...")

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    print(f"\n--- {file_name} taranıyor ---")
    with open(file_name, 'r', encoding='utf-8') as f:
        try:
            items = json.load(f)
            # Liste değilse (Örn: sözlükse) listeye çevir
            if isinstance(items, dict):
                for k in items:
                    if isinstance(items[k], list): items = items[k]; break
            
            for item in items:
                if not isinstance(item, dict): continue
                pid = item.get('id')
                name = item.get('model') or item.get('name')
                
                if pid and name:
                    # GHz vb. kısımları silerek aramayı kolaylaştır
                    search_name = str(name).split('GHz')[0].split('Cache')[0].strip()
                    print(f"Aranıyor: {search_name}")
                    
                    try:
                        res = requests.get(f"{GOOGLE_PROXY}?name={requests.utils.quote(search_name)}", timeout=30)
                        price_text = res.text.strip()
                        
                        if "Bulunamadi" not in price_text and "Hata" not in price_text and len(price_text) < 50:
                            results[pid] = {"price_tr": price_text}
                            print(f"  [OK] Bulundu: {price_text}")
                        else:
                            print(f"  [!] Bilgi: {price_text[:30]}")
                            
                    except:
                        print("  [X] Google'a ulasilamadi.")
                    
                    time.sleep(1) # Banlanmamak için
        except Exception as e:
            print(f"HATA: {e}")

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nISLEM BITTI! updates.json içine {len(results)} ürün kaydedildi.")
