import requests, json, os, time

GOOGLE_PROXY = "https://script.google.com/macros/s/AKfycbwDfPQRamV9dnyxGRd_6KmeViUjJ0ZGywoa5f7mw0rUsr5cQkQ_kzQ2QSrlCI607Hdc/exec"

DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'rams.json', 'sata_ssds.json', 'hdds.json', 'psus.json', 'monitors.json']
results = {}

def get_numeric(p_str):
    try:
        return int("".join(filter(str.isdigit, p_str.split(',')[0])))
    except: return 0

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    print(f"\n--- {file_name} taranıyor ---")
    with open(file_name, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            items = data if isinstance(data, list) else []
            for item in items:
                if not isinstance(item, dict): continue
                pid = item.get('id')
                name = item.get('model') or item.get('name')
                
                if pid and name:
                    print(f"Sorgulanıyor: {name}")
                    try:
                        # Google'dan gelen ham cevabı al
                        res = requests.get(f"{GOOGLE_PROXY}?name={requests.utils.quote(str(name))}", timeout=45)
                        raw_response = res.text.strip()
                        
                        if "Bulunamadi" not in raw_response and "Hata" not in raw_response:
                            results[pid] = {"price_tr": raw_response}
                            print(f"  [OK] Fiyat: {raw_response}")
                        else:
                            # Hatanın ne olduğunu ekrana yazdır
                            print(f"  [!] Bilgi: {raw_response}")
                            
                    except Exception as e:
                        print(f"  [X] Baglanti Hatasi: {e}")
                    
                    time.sleep(1.2) # Banlanmamak için
        except Exception as e:
            print(f"HATA: {e}")

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nISLEM BITTI! {len(results)} urun kaydedildi.")
