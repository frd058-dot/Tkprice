import requests, json, os, time

GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycbzQHICP8Yldkcl5L_rwpJ6mnvA9T3XqCfMmaad2c7qmwZnM1U3lZm2Vk4i6nkirRknpBg/exec"

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
    name = str(name).replace("(Workstation)", "").replace("(2024)", "").replace("(2025)", "")
    if level == 2:
        for word in ["White", "Black", "Challenger", "Gaming OC", "Steel Legend", "Dual", "OC"]:
            name = name.replace(word, "")
    if level == 3:
        words = name.split()
        return " ".join(words[:3])
    return name.strip()

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    print(f"\n--- {file_name} ---")
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
                
                found_price = None
                for lvl in [1, 2, 3]:
                    search_term = clean_name_advanced(full_name, level=lvl)
                    found_price = fetch_price(search_term)
                    if found_price: break
                    time.sleep(0.5)

                if found_price:
                    # Rakamı çekip kontrol et
                    clean_digit = "".join(filter(str.isdigit, found_price.split(',')[0]))
                    numeric_price = int(clean_digit) if clean_digit else 0
                    
                    if numeric_price > 500:
                        results[pid] = {"price_tr": found_price}
                        print(f"    => OK: {found_price}")
                    else:
                        print(f"    => Gecersiz: {found_price}")
                else:
                    print(f"    => BULUNAMADI")
                
                time.sleep(0.8)
    except Exception as e:
        print(f"Hata: {e}")

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nISLEM BITTI! Toplam {len(results)} urun guncellendi.")
