import requests
from bs4 import BeautifulSoup
import json
import time
import os
# scraper.py en başlarına ekleyin
print(f"Mevcut dizindeki dosyalar: {os.listdir('.')}")

# TARANACAK DOSYALAR (GitHub deponuza bu dosyaları yüklemelisiniz)
DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'hdds.json', 'imacs.json', 'mac_minis.json', 'monitors.json', 
              'monitors.json', 'notebook_configs.json', 'psus.json', 'rams.json', 'sata_ssds.json', 'storages.json' ]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

def get_price_epey(name):
    try:
        url = f"https://www.epey.com/ara/?ara={name}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.find('span', class_='urun-fiyat').text.strip()
    except: return None

def get_price_amazon(name, domain="com"): # "com" for USA, "de" for EU
    # Amazon bot koruması nedeniyle bazen boş dönebilir
    return None # Şimdilik Epey odaklı gidelim veya Amazon API ekleyelim

results = {}

# 1. JSON dosyalarını oku ve tüm ürünleri listeye al
for file_name in DATA_FILES:
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            items = json.load(f)
            for item in items:
                pid = item.get('id')
                name = item.get('model') or item.get('name') or item.get('title')
                
                if pid and name:
                    print(f"Aranıyor: {name}...")
                    price_tr = get_price_epey(name)
                    
                    if price_tr:
                        results[pid] = {"price_tr": price_tr}
                        print(f"Bulundu: {price_tr}")
                    
                    # Sitelerden banlanmamak için bekle
                    time.sleep(1.5)

# 2. Hepsini tek bir updates.json dosyasında topla
with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
