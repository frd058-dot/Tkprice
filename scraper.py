import requests
import json
import os
import time

# 1. Adımdaki linki buraya yapıştırın
GOOGLE_API_URL = "BURAYA_GOOGLE_SCRIPT_LINKINIZI_YAPISTIRIN"

results = {}
json_files = [f for f in os.listdir('.') if f.endswith('.json') and f != 'updates.json']

print(f"BAŞLATILIYOR: Toplam {len(json_files)} dosya taranacak.")

for file_name in json_files:
    print(f"\n--- {file_name} İşleniyor ---")
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            items = json.load(f)
            if isinstance(items, dict):
                for k in items:
                    if isinstance(items[k], list): items = items[k]; break
            
            for item in items:
                pid = item.get('id')
                name = item.get('model') or item.get('name')
                
                if pid and name:
                    # Google köprüsü üzerinden fiyat sorgula
                    res = requests.get(f"{GOOGLE_API_URL}?name={name}")
                    if res.status_code == 200 and res.text != "Bulunamadı":
                        results[pid] = {"price_tr": res.text}
                        print(f"  -> {name}: {res.text}")
                    else:
                        print(f"  -> {name}: Fiyat Çekilemedi")
                    
                    time.sleep(0.5) # İşlemi hızlandırmak için bekleme süresini düşürdük
    except: continue

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nFİYAT GÜNCELLEME TAMAMLANDI!")
