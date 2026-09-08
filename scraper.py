import requests, json, os, time

# BURAYA 1. ADIMDA ALDIĞINIZ TERTEMİZ YENİ LİNKİ YAPIŞTIRIN
GOOGLE_PROXY_URL = "https://script.google.com/macros/s/AKfycbw2UswJ223WHjWbBToYkFIHyHXdue4TX8q4mXIiyp58i0OY_zYHcR3z4y1MHYruLlMndQ/exec"

DATA_FILES = ['cpu.json', 'gpus.json', 'notebooks.json', 'aio_configs.json', 'cases.json', 'coolers.json', 'rams.json', 'psus.json']
results = {}

def get_clean_price(name, region):
    try:
        url = f"{GOOGLE_PROXY_URL}?name={requests.utils.quote(name)}&region={region}"
        res = requests.get(url, timeout=30)
        # Eğer Google hata verip HTML döndürürse bunu atla
        if res.text.startswith("<!DOCTYPE") or "Bulunamadı" in res.text:
            return None
        return res.text.strip()
    except: return None

for file_name in DATA_FILES:
    if not os.path.exists(file_name): continue
    print(f"\n--- {file_name} İşleniyor ---")
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        items = data if isinstance(data, list) else []
        if isinstance(data, dict):
            for k in data:
                if isinstance(data[k], list): items = data[k]; break

        for item in items:
            if not isinstance(item, dict): continue
            pid = item.get('id')
            # Aramayı bozmasın diye GHz vb. detayları isimden atıyoruz
            name = (item.get('model') or item.get('name')).split('GHz')[0].split('Cache')[0].strip()
            
            if pid and name:
                print(f"Sorgu: {name}")
                results[pid] = {}
                
                # TR, USA ve EU fiyatlarını sırayla çek
                results[pid]["price_tr"] = get_clean_price(name, "tr")
                results[pid]["price_usd"] = get_clean_price(name, "usa")
                results[pid]["price_eur"] = get_clean_price(name, "eu")
                
                print(f"  -> TR: {results[pid]['price_tr']} | USA: {results[pid]['price_usd']} | EU: {results[pid]['price_eur']}")
                time.sleep(1)

with open('updates.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nİŞLEM TAMAM! updates.json dünya geneli fiyatlarla güncellendi.")
