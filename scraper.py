import requests, json, os, time

GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycbzQHICP8Yldkcl5L_rwpJ6mnvA9T3XqCfMmaad2c7qmwZnM1U3lZm2Vk4i6nkirRknpBg/exec"

# Taranacak tüm veri dosyaları
DATA_FILES = [
    'cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 
    'cases.json', 'coolers.json', 'rams.json', 'sata_ssds.json', 
    'hdds.json', 'psus.json', 'monitors.json'
]

results = {}

def create_precise_search_name(item):
    """Marka ve Model bilgilerini akıllıca birleştirir"""
    brand = str(item.get('brand', '')).strip()
    # Model, name veya title alanlarından en uzun/detaylı olanı seçelim
    model = str(item.get('model') or item.get('name') or item.get('title', '')).strip()
    
    # Eğer marka zaten model isminin içinde geçiyorsa (Örn: 'ASUS ROG RTX 4060')
    # markayı tekrar ekleyip aramayı bozmayalım.
    if brand.lower() in model.lower():
        full_name = model
    else:
        full_name = f"{brand} {model}"
    
    # Epey'i yanıltan 'GHz', 'Cache', 'LGA1700' gibi teknik detayları temizle
    # Ama 'OC', 'Prime', 'Dual', 'Gaming' gibi model belirteçlerini KORU.
    clean_name = full_name.split('GHz')[0].split('Cache')[0].split('Socket')[0].strip()
    return clean_name

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    print(f"\n--- {file_name} taranıyor ---")
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
                
                if pid:
                    # NOKTA ATIŞI İSİM OLUŞTURMA
                    search_name = create_precise_search_name(item)
                    print(f"Aranıyor: {search_name}")
                    
                    try:
                        # Google Proxy üzerinden sorgula
                        res = requests.get(f"{GOOGLE_PROXY_URL}?name={requests.utils.quote(search_name)}", timeout=30)
                        if "Bulunamadı" not in res.text and "Hata" not in res.text:
                            price = res.text.strip()
                            results[pid] = {"price_tr": price}
                            print(f"  => OK: {price}")
                        else:
                            # Eğer çok detaylı isimle bulunamadıysa, bir de markasız sadece modeli dene
                            print(f"  => Detaylı isimle bulunamadı, bekleniyor...")
                    except: pass
                    time.sleep(0.8) # Güvenli tarama hızı
    except Exception as e:
        print(f"Dosya hatası: {e}")

# updates.json'a kaydet
with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nİŞLEM BİTTİ! updates.json güncellendi.")
