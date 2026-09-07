import requests
from bs4 import BeautifulSoup
import json
import time
import os
import random

# Tarayıcı başlıklarını çeşitlendiriyoruz (Engeli aşmak için kritik)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
]

def get_price_tr(name):
    """Epey engellerini aşmaya çalışan gelişmiş tarayıcı"""
    try:
        url = f"https://www.epey.com/ara/?ara={requests.utils.quote(name)}"
        
        # Her aramada farklı bir kimlik kullan
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        # Session kullanarak çerez yönetimini sağla
        session = requests.Session()
        res = session.get(url, headers=headers, timeout=20)
        
        if res.status_code != 200:
            return None
            
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Epey'deki olası tüm fiyat etiketlerini sırayla kontrol et
        selectors = [
            ('span', 'urun-fiyat'), # Ürün sayfasındaki ana fiyat
            ('span', 'fyt'),        # Arama listesindeki fiyatlar
            ('div', 'fiyat'),       # Alternatif liste fiyatı
            ('a', 'fiyat')          # Link içindeki fiyat
        ]
        
        for tag, class_name in selectors:
            found = soup.find(tag, class_=class_name)
            if found and found.text.strip():
                price = found.text.strip()
                if "TL" in price or "₺" in price:
                    return price
        
    except Exception as e:
        print(f"  !! Hata: {e}")
    return None

results = {}
json_files = [f for f in os.listdir('.') if f.endswith('.json') and f != 'updates.json']

print(f"Başlatılıyor... Toplam dosya: {len(json_files)}")

for file_name in json_files:
    print(f"\n--- {file_name} İşleniyor ---")
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            items = json.load(f)
            if isinstance(items, dict): # Bazı JSON formatları için destek
                for k in items:
                    if isinstance(items[k], list): items = items[k]; break
            
            # Sadece ilk 20 ürünü deneyelim (Test amaçlı ve banlanmamak için)
            # İleride her şeyi çekmek için [:20] kısmını silebilirsin
            for item in items[:20]:
                pid = item.get('id')
                name = item.get('model') or item.get('name')
                
                if pid and name:
                    print(f"Aranıyor: {name}")
                    price = get_price_tr(name)
                    if price:
                        results[pid] = {"price_tr": price}
                        print(f"  -> Bulundu: {price}")
                    else:
                        print(f"  -> Bulunamadı")
                    
                    # Çok önemli: Epey bizi kovmasın diye rastgele bekleme yapıyoruz
                    time.sleep(random.uniform(2, 4))
                    
    except Exception as e:
        print(f"Dosya Hatası: {e}")

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nBİTTİ! {len(results)} ürün güncellendi.")
