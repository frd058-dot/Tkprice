import requests
from bs4 import BeautifulSoup
import json
import time
import os

# Tarayıcı gibi görünmek için başlıklar
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

def get_price_tr(name):
    """Epey.com üzerinden fiyat çeker (Farklı etiketleri kontrol eder)"""
    try:
        url = f"https://www.epey.com/ara/?ara={name}"
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code != 200: return None
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 1. Seçenek: urun-fiyat (Ürün sayfası veya belirgin sonuç)
        price = soup.find('span', class_='urun-fiyat')
        if price: return price.text.strip()
        
        # 2. Seçenek: fyt (Arama listesindeki fiyatlar)
        price = soup.find('span', class_='fyt')
        if price: return price.text.strip()
        
    except: return None
    return None

results = {}

# 1. Dizindeki tüm JSON dosyalarını otomatik bul (updates.json hariç)
json_files = [f for f in os.listdir('.') if f.endswith('.json') and f != 'updates.json']

print(f"Bulunan veri dosyaları: {json_files}")

for file_name in json_files:
    print(f"\n--- {file_name} İŞLENİYOR ---")
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Veri listeyse doğrudan kullan, sözlükse içindeki listeleri bul
            items = []
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                # Sözlük içindeki ilk listeyi bulmaya çalış (cpus, gpus vb.)
                for key in data:
                    if isinstance(data[key], list):
                        items = data[key]
                        break
                if not items and 'id' in data: # Tek bir ürün objesiyse
                    items = [data]

            print(f"Dosya içinden {len(items)} ürün okundu.")

            for item in items:
                # ID ve İsim yakalama (Büyük/küçük harf duyarsız)
                pid = item.get('id')
                name = item.get('model') or item.get('name') or item.get('title') or item.get('model_name')
                
                if pid and name:
                    print(f"Aranıyor: {name} (ID: {pid})")
                    price = get_price_tr(name)
                    if price:
                        results[pid] = {"price_tr": price}
                        print(f"  -> BULDUM: {price}")
                    else:
                        print(f"  -> Fiyat çekilemedi (Epey'de bulunamadı veya bot engellendi)")
                    
                    time.sleep(1.5) # Güvenlik için bekleme
    except Exception as e:
        print(f"HATA ({file_name}): {e}")

# 2. Sonuçları updates.json'a yaz
with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nİŞLEM TAMAMLANDI!")
print(f"updates.json içine toplam {len(results)} ürün kaydedildi.")
