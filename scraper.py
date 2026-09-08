import requests, json, os, time

GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycby5vYwgNG5olOnIKpnqeKu1ly6dFLDLbu8NY4ahpdmqVNn9M_9T-cj2y35J-WGVoxVKZA/exec"

# Taranacak dosyalar
DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'rams.json', 'storages.json']
results = {}

def clean_name(name):
    """Ürün ismini Epey'in bulabileceği kadar sadeleştirir"""
    name = str(name).lower()
    # Gereksiz detayları temizle
    for word in ["ghz", "cache", "lga1700", "am4", "am5", "v2", "v3", "pro", "plus"]:
        name = name.split(word)[0]
    # Sadece ilk 3 kelimeyi al (Genelde Marka + Seri + Model yeterlidir)
    words = name.split()
    return " ".join(words[:3]).strip()

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
                raw_name = item.get('model') or item.get('name') or item.get('title')
                
                if pid and raw_name:
                    # İSMİ SADELEŞTİREREK ARAT
                    search_name = clean_name(raw_name)
                    print(f"Sorgulanıyor: {search_name} (Orijinal: {raw_name[:20]}...)")
                    
                    try:
                        res = requests.get(f"{GOOGLE_PROXY_URL}?name={requests.utils.quote(search_name)}", timeout=25)
                        if res.status_code == 200 and "Bulunamadı" not in res.text:
                            price = res.text.strip()
                            results[str(pid)] = {"price_tr": price}
                            print(f"  => BULDUM: {price}")
                        else:
                            print(f"  => Bulunamadı")
                    except: pass
                    time.sleep(0.4)
        except: continue

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nBİTTİ! updates.json doluluk: {len(results)}")
