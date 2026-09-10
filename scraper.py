import requests, json, os, time

API_KEY = os.getenv('SCRAPER_API_KEY')

def get_price_from_google(name):
    """Google Arama Sonuçlarındaki fiyatı ScraperAPI ile yakalar"""
    try:
        # STRATEJİ: Google'da fiyatı aratıyoruz (En hatasız yöntem budur)
        query = requests.utils.quote(f"{name} fiyatı")
        target_url = f"https://www.google.com/search?q={query}"
        
        # ScraperAPI üzerinden Google'a giriyoruz (Engel yok!)
        proxy_url = f"http://api.scraperapi.com?api_key={API_KEY}&url={target_url}&country_code=tr"
        
        res = requests.get(proxy_url, timeout=60)
        if res.status_code == 200:
            import re
            # Google arama sonucundaki "12.500,00 TL" veya "12.500 ₺" kalıbını bulur
            content = res.text
            # Taksit/aylık gibi çöp verileri temizle
            content = content.replace("taksit", "XXX").replace("aylık", "XXX")
            
            # Fiyat Regex'i (TL ve ₺ odaklı)
            price_match = re.search(r'(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s?(?:TL|₺)', content)
            
            if price_match:
                return price_match.group(0).strip()
    except Exception as e:
        print(f"  !! Hata: {e}")
    return None

results = {}
json_files = [f for f in os.listdir('.') if f.endswith('.json') and f != 'updates.json']

for file_name in json_files:
    print(f"\n--- {file_name} İşleniyor ---")
    with open(file_name, 'r', encoding='utf-8') as f:
        try:
            items = json.load(f)
            # Ürün sayısını sınırlayarak test edelim (Limitleri harcamamak için)
            for item in items[:15]: 
                pid = item.get('id')
                # İsmi biraz sadeleştirelim ki Google daha kolay bulsun
                raw_name = item.get('model') or item.get('name')
                name = str(raw_name).split('GHz')[0].split('Cache')[0].strip()
                
                if pid and name:
                    print(f"Google'a Soruluyor: {name}")
                    price = get_price_from_google(name)
                    if price:
                        results[pid] = {"price_tr": price}
                        print(f"  [BULDUM] {price}")
                    else:
                        print("  [YOK] Google'da bulunamadı")
                    time.sleep(1)
        except: continue

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nTAMAMLANDI! Fiyatlar başarıyla toplandı.")
