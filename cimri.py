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
    
    # Streamlit Cloud'da Chromium'un standart yolu
    options.binary_location = "/usr/bin/chromium"
    
    # Sürücüyü sisteme kurulu olan chromium-driver üzerinden başlatıyoruz
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
        wait = WebDriverWait(driver, 15)
        
        # Dükkan isimlerini bul (Google'ın güncel dükkan başlığı sınıfı: qBF1Pd)
        time.sleep(5)
        places = driver.find_elements(By.CLASS_NAME, "qBF1Pd")
        
        for place in places[:limit]:
            name = place.text
            if name:
                results.append({"Dükkan Adı": name})
                
    except Exception as e:
        st.error(f"Teknik bir hata oluştu: {e}")
    finally:
        if driver:
            driver.quit()
            
    return results

# Arayüz Tasarımı
st.title("🕵️‍♂️ Profesyonel Bölgesel Satıcı Kaşifi")
st.info("Bu araç, belirttiğiniz bölgedeki satıcıları tarayarak size listeler.")

# Yan Menü (Sidebar)
st.sidebar.header("🔍 Arama Ayarları")
search_query = st.sidebar.text_input("Ne arıyorsunuz?", "Koli Bandı")
location_query = st.sidebar.text_input("Hangi bölgede?", "İstoç")
target_count = st.sidebar.slider("Hedeflenen dükkan sayısı", 5, 50, 15)

if st.sidebar.button("Derin Taramayı Başlat"):
    if search_query and location_query:
        with st.spinner(f"{location_query} bölgesinde {search_query} satıcıları taranıyor..."):
            data = gmaps_search(search_query, location_query, target_count)
            
            if data:
                df = pd.DataFrame(data)
                st.success(f"{len(df)} dükkan başarıyla listelendi!")
                st.table(df)
                
                # Excel/CSV İndirme
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("Sonuçları İndir", csv, "saticilar.csv", "text/csv")
            else:
                st.warning("Sonuç bulunamadı. Lütfen arama kelimelerini kontrol edin.")
    else:
        st.error("Lütfen tüm alanları doldurun.")

st.markdown("---")
st.caption("© 2025 enucuzuburda.com.tr")
