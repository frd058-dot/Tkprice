import requests, json, os, time

GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycbzQHICP8Yldkcl5L_rwpJ6mnvA9T3XqCfMmaad2c7qmwZnM1U3lZm2Vk4i6nkirRknpBg/exec"

# Taranacak tüm dosyalar
DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'rams.json', 'sata_ssds.json', 'hdds.json', 'psus.json', 'monitors.json']
results = {}

def fetch_price(name):
    try:
        res = requests.get(f"{GOOGLE_PROXY_URL}?name={requests.utils.quote(name)}", timeout=35)
        if res.status_code == 200 and "Bulunamadı" not in res.text and "Hata" not in res.text:
            return res.text.strip()
    except: pass
    return None

def clean_name_advanced(name, level=1):
    """İsmi kademeli olarak temizler"""
    name = str(name).replace("(Workstation)", "").replace("(2024)", "").replace("(2025)", "")
    if level == 2:
        # Renkleri ve özel takıları temizle
        for word in ["White", "Black", "Challenger", "Gaming OC", "Steel Legend", "Dual", "OC"]:
            name = name.replace(word, "")
    if level == 3:
        # Sadece temel marka ve model kalsın
        words = name.split()
        return " ".join(words[:3])
    return name.strip()

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    print(f"\n--- {file_name} İşleniyor ---")
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
                
                if not pid or not model: continue
                
                full_name = model if brand.lower() in model.lower() else f"{brand} {model}"
                
                # KADEMELİ ARAMA
                found_price = None
                for lvl in [1, 2, 3]:
                    search_term = clean_name_advanced(full_name, level=lvl)
                    if lvl > 1: print(f"  -> Tekrar Deneniyor (Lvl {lvl}): {search_term}")
                    else: print(f"Aranıyor: {search_term}")
                    
                    found_price = fetch_price(search_term)
                    if found_price: break # Bulunduysa döngüden çık
                    time.sleep(0.5)

                if found_price:
                    results[pid] = {"price_tr": found_price}
                    print(f"    => TAMAM: {found_price}")
                else:
                    print(f"    => BULUNAMADI")
                
                time.sleep(1) # Siteyi korumak için
    except Exception as e:
        print(f"Hata: {e}")

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nİŞLEM TAMAMLANDI! Toplam {len(results)} ürün güncellendi.")import requests, json, os, time

GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycbzQHICP8Yldkcl5L_rwpJ6mnvA9T3XqCfMmaad2c7qmwZnM1U3lZm2Vk4i6nkirRknpBg/exec"

# Taranacak tüm dosyalar
DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'rams.json', 'sata_ssds.json', 'hdds.json', 'psus.json', 'monitors.json']
results = {}

def fetch_price(name):
    try:
        res = requests.get(f"{GOOGLE_PROXY_URL}?name={requests.utils.quote(name)}", timeout=35)
        if res.status_code == 200 and "Bulunamadı" not in res.text and "Hata" not in res.text:
            return res.text.strip()
    except: pass
    return None

def clean_name_advanced(name, level=1):
    """İsmi kademeli olarak temizler"""
    name = str(name).replace("(Workstation)", "").replace("(2024)", "").replace("(2025)", "")
    if level == 2:
        # Renkleri ve özel takıları temizle
        for word in ["White", "Black", "Challenger", "Gaming OC", "Steel Legend", "Dual", "OC"]:
            name = name.replace(word, "")
    if level == 3:
        # Sadece temel marka ve model kalsın
        words = name.split()
        return " ".join(words[:3])
    return name.strip()

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    print(f"\n--- {file_name} İşleniyor ---")
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
                
                if not pid or not model: continue
                
                full_name = model if brand.lower() in model.lower() else f"{brand} {model}"
                
                # KADEMELİ ARAMA
                found_price = None
                for lvl in [1, 2, 3]:
                    search_term = clean_name_advanced(full_name, level=lvl)
                    if lvl > 1: print(f"  -> Tekrar Deneniyor (Lvl {lvl}): {search_term}")
                    else: print(f"Aranıyor: {search_term}")
                    
                    found_price = fetch_price(search_term)
                    if found_price: break # Bulunduysa döngüden çık
                    time.sleep(0.5)

                if found_price:
                    results[pid] = {"price_tr": found_price}
                    print(f"    => TAMAM: {found_price}")
                else:
                    print(f"    => BULUNAMADI")
                
                time.sleep(1) # Siteyi korumak için
    except Exception as e:
        print(f"Hata: {e}")

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nİŞLEM TAMAMLANDI! Toplam {len(results)} ürün güncellendi.")
