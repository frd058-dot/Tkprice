import requests
from bs4 import BeautifulSoup
import json
import time
import os
import random

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
}

def get_price_akakce(name):
    """Akakçe üzerinden fiyat aramayı dener"""
    try:
        # Arama terimini temizle ve encode et
        query = requests.utils.quote(name)
        url = f"https://www.akakce.com/arama/?q={query}"
        
        res = requests.get(url, headers=HEADERS, timeout=15)
        
        # TEŞHİS: Sayfa yüklendi mi?
        print(f"  [Akakce] Durum: {res.status_code}")
        
        if res.status_code == 403:
            print("  !! Hata: Site erişimi engelledi (403 Forbidden)")
            return None

        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Sayfa başlığını kontrol et (Engelleme sayfası mı?)
        title = soup.title.text if soup.title else "Başlık Yok"
        print(f"  [Akakce] Sayfa Başlığı: {title[:30]}")

        # Akakçe fiyat etiketini ara (Genelde span.pt_v8 veya b.p_v8)
        price_tag = soup.select_one('span.pt_v8, span.p_v8, b.p_v8')
        if price_tag:
            return price_tag.text.strip()
            
    except Exception as e:
        print(f"  !! Akakce Hatası: {e}")
    return None

results = {}
json_files = [f for f in os.listdir('.') if f.endswith('.json') and f != 'updates.json']

print(f"Sistem Kontrolü: {len(json_files)} dosya taranacak.")

for file_name in json_files:
    print(f"\n--- {file_name} taranıyor ---")
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            items = json.load(f)
            if isinstance(items, dict):
                for k in items:
                    if isinstance(items[k], list): items = items[k]; break
            
            # Ürün sayısını sınırla (Engellenmemek için ilk 10 ürünle test et)
            for item in items[:10]:
                pid = item.get('id')
                name = item.get('model') or item.get('name')
                
                if pid and name:
                    # Uzun isimleri kısaltalım (Arama başarısı için)
                    short_name = " ".join(name.split()[:4])
                    print(f"\nAranıyor: {short_name}")
                    
                    price = get_price_akakce(short_name)
                    if price:
                        results[pid] = {"price_tr": price}
                        print(f"  => BAŞARILI: {price}")
                    else:
                        print("  => BAŞARISIZ: Fiyat bulunamadı.")
                    
                    time.sleep(random.uniform(3, 5))
                    
    except Exception as e:
        print(f"Hata: {e}")

# updates.json'u kaydet
with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nİşlem bitti. updates.json doluluk oranı: {len(results)}")
