import requests
from bs4 import BeautifulSoup
import json
import time
import os

# TARANACAK DOSYALAR (GitHub deponda olanları okur, olmayanları geçer)
DATA_FILES = [
    'cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 
    'cases.json', 'coolers.json', 'hdds.json', 'imacs.json', 
    'mac_minis.json', 'monitors.json', 'notebook_configs.json', 
    'psus.json', 'rams.json', 'sata_ssds.json', 'storages.json', 'macbooks.json'
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

def get_price_tr(name):
    """Epey.com üzerinden Türkiye fiyatını çeker"""
    try:
        url = f"https://www.epey.com/ara/?ara={name}"
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            price = soup.find('span', class_='urun-fiyat')
            if price: return price.text.strip()
    except: return None
    return None

def get_price_amazon(name, domain="com"):
    """Amazon (.com veya .de) üzerinden Global fiyat çeker"""
    try:
        url = f"https://www.amazon.{domain}/s?k={name}"
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            whole = soup.find('span', class_='a-price-whole')
            if whole:
                symbol = "$" if domain == "com" else "€"
                return f"{whole.text.strip()}{symbol}"
    except: return None
    return None

results = {}
print(f"Dizin kontrolü: {os.listdir('.')}")

for file_name in DATA_FILES:
    if not os.path.exists(file_name):
        print(f"Atlanıyor (Dosya Yok): {file_name}")
        continue

    print(f"\n--- {file_name} İşleniyor ---")
    with open(file_name, 'r', encoding='utf-8') as f:
        try:
            items = json.load(f)
            # Eğer dosya bir nesne ise ve içinde liste varsa (örn: {"items": [...]})
            if isinstance(items, dict):
                items = items.get('items', []) or items.get('cpus', []) or items.get('gpus', [])
            
            for item in items:
                pid = item.get('id')
                # İsim alanını farklı anahtarlarda ara
                name = item.get('model') or item.get('name') or item.get('title')
                
                if pid and name:
                    print(f"Aranıyor: {name}...")
                    p_tr = get_price_tr(name)
                    # p_usa = get_price_amazon(name, "com") # Opsiyonel: USA için açılabilir
                    # p_eu = get_price_amazon(name, "de")  # Opsiyonel: EU için açılabilir

                    if p_tr:
                        results[pid] = {"price_tr": p_tr}
                        # if p_usa: results[pid]["price_usd"] = p_usa
                        # if p_eu: results[pid]["price_eur"] = p_eu
                        print(f"Bulundu: {p_tr}")
                    
                    time.sleep(1.2) # Banlanmamak için kısa bekleme
        except Exception as e:
            print(f"HATA ({file_name}): {e}")

# updates.json dosyasını kaydet
with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nİşlem bitti! updates.json içine {len(results)} ürün kaydedildi.")
