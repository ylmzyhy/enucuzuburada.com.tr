import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Sayfa Yapılandırması
st.set_page_config(page_title="En Ucuzu Burada - Satıcı Kaşifi", layout="wide")

def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/usr/bin/chromium"
    
    service = Service("/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)

def gmaps_search(query, location, limit):
    driver = None
    results = []
    
    try:
        driver = init_driver()
        # Google Haritalar arama URL'si
        search_url = f"https://www.google.com/maps/search/{query}+{location}"
        driver.get(search_url)
        
        # Sayfanın yüklenmesi için bekleme
        time.sleep(5)
        
        # Dükkan kartlarını bul (Haritalar dükkan konteyneri: Nv2Ybe veya hfpxzc)
        places = driver.find_elements(By.CLASS_NAME, "Nv2Ybe")
        
        # Eğer yukarıdaki sınıf değiştiyse yedek sınıfı dene
        if not places:
            places = driver.find_elements(By.CLASS_NAME, "hfpxzc")

        for place in places[:limit]:
            try:
                # İsim ve Detaylı Link (Haritalar Linki)
                # Google genellikle dükkan linkini hfpxzc sınıfındaki 'href' içine koyar
                link = place.get_attribute("href")
                name = place.get_attribute("aria-label")
                
                # Kart içindeki metni alarak Adres ve Telefonu ayırmaya çalışalım
                full_text = place.text.split("\n")
                
                # Basit bir eşleştirme mantığı:
                # Genellikle: [İsim, Puan, Adres, Kapalı/Açık, Telefon] şeklinde gelir
                address = "Bilinmiyor"
                phone = "Bilinmiyor"
                
                for line in full_text:
                    if "05" in line or "02" in line or "08" in line: # Telefon numarası tespiti
                        phone = line
                    elif len(line) > 15 and name not in line: # Uzun metinler genellikle adrestir
                        address = line

                results.append({
                    "Dükkan Adı": name,
                    "Adres": address,
                    "Telefon": phone,
                    "Harita Linki": link
                })
            except:
                continue
                
    except Exception as e:
        st.error(f"Teknik bir hata oluştu: {e}")
    finally:
        if driver:
            driver.quit()
            
    return results

# Arayüz Tasarımı
st.title("🕵️‍♂️ Profesyonel Bölgesel Satıcı Kaşifi")
st.info("Bu araç, belirttiğiniz bölgedeki satıcıları tarayarak adres ve telefon bilgileriyle listeler.")

# Yan Menü
st.sidebar.header("🔍 Arama Ayarları")
search_query = st.sidebar.text_input("Ne arıyorsunuz?", "Koli Bandı")
location_query = st.sidebar.text_input("Hangi bölgede?", "İstoç")
target_count = st.sidebar.slider("Hedeflenen dükkan sayısı", 5, 50, 15)

if st.sidebar.button("Derin Taramayı Başlat"):
    if search_query and location_query:
        with st.spinner("Veriler toplanıyor, bu işlem biraz sürebilir..."):
            data = gmaps_search(search_query, location_query, target_count)
            
            if data:
                df = pd.DataFrame(data)
                st.success(f"{len(df)} dükkan bilgisi başarıyla çekildi!")
                
                # Tabloyu göster
                st.dataframe(df, use_container_width=True)
                
                # Excel/CSV İndirme
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("Excel (CSV) Olarak İndir", csv, "saticilar_detayli.csv", "text/csv")
            else:
                st.warning("Sonuç bulunamadı. Lütfen arama kelimelerini (Örn: 'Koli Bandı Toptan') zenginleştirin.")
    else:
        st.error("Lütfen tüm alanları doldurun.")

st.markdown("---")
st.caption("© 2025 enucuzuburda.com.tr")
