import requests, json, os, time

# Sizin görseldeki GERÇEK Google Proxy linkiniz
GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycbxWppt-80fiTCRyk-2xbORlmSBF-huZKhc8jpZMfR1VAblwwJw2Dw5lOE7aUw-owUbfVA/exec"

# Tüm donanım dosyalarınız (Bu dosyalar GitHub Tkprice deposunda duruyor)
DATA_FILES = [
    'cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 
    'cases.json', 'coolers.json', 'hdds.json', 'imacs.json', 
    'mac_minis.json', 'macbooks.json', 'monitors.json', 
    'motherboard.json', 'notebook_configs.json', 'psus.json', 
    'rams.json', 'sata_ssds.json', 'storages.json'
]

results = {}

print(f"BAŞLATILIYOR... Toplam {len(DATA_FILES)} dosya taranacak.")

for file_name in DATA_FILES:
    if not os.path.exists(file_name):
        print(f"Atlanıyor (Dosya bulunamadı): {file_name}")
        continue
    
    print(f"\n--- {file_name} İşleniyor ---")
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Liste formatı mı yoksa obje formatı mı kontrol et
            items = []
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                for k in data:
                    if isinstance(data[k], list): items.extend(data[k])
            
            for item in items:
                if not isinstance(item, dict): continue
                
                pid = item.get('id')
                # Ürün adını en sade haliyle al (i3-12100f gibi)
                raw_name = item.get('model') or item.get('name') or item.get('title')
                
                if pid and raw_name:
                    # GHz, MB gibi gereksiz detayları silip Google'a gönder
                    search_name = str(raw_name).split('GHz')[0].split('Cache')[0].strip()
                    print(f"Aranıyor: {search_name}")
                    
                    try:
                        res = requests.get(f"{GOOGLE_PROXY_URL}?name={requests.utils.quote(search_name)}", timeout=30)
                        
                        if res.status_code == 200 and "Bulunamadı" not in res.text and "Hata" not in res.text:
                            price_val = res.text.strip()
                            results[str(pid)] = {"price_tr": price_val}
                            print(f"  => OK: {price_val}")
                        else:
                            print(f"  => Bulunamadı")
                    except:
                        print(f"  => Sorgu Hatası")
                    
                    # Her ürün arası kısa bir bekleme (Sistemi yormamak için)
                    time.sleep(0.5)
                    
    except Exception as e:
        print(f"Dosya okuma hatası: {e}")

# updates.json dosyasını deponun ana dizinine kaydet
with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nİŞLEM BİTTİ! updates.json içine {len(results)} ürün kaydedildi.")
