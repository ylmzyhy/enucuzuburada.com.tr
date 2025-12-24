import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Sayfa Yapılandırması
st.set_page_config(page_title="En Ucuzu Burada - Satıcı Kaşifi", layout="wide")

# Sidebar - Arama Ayarları
st.sidebar.header("🔍 Arama Ayarları")
search_query = st.sidebar.text_input("Ne arıyorsunuz?", placeholder="Örn: Koli Bandı")
location_query = st.sidebar.text_input("Hangi bölgede?", placeholder="Örn: İstoç")
target_count = st.sidebar.slider("Hedeflenen dükkan sayısı", 5, 50, 15)

def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    # Streamlit Cloud'daki Chromium'un standart yolu
    options.binary_location = "/usr/bin/chromium"
    
    # Sürücü kurulumunu en güvenli yöntemle yapıyoruz
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def gmaps_search(query, location, limit):
    driver = init_driver()
    results = []
    
    try:
        # Google Haritalar arama linki
        search_url = f"https://www.google.com/maps/search/{query}+{location}"
        driver.get(search_url)
        
        wait = WebDriverWait(driver, 15)
        
        # Sonuçların yüklenmesi için biraz bekle
        time.sleep(5)
        
        # Dükkan isimlerini topla
        # Not: Google seçicileri sık değişebilir, en genel seçiciyi kullanıyoruz
        places = driver.find_elements(By.CSS_SELECTOR, "div.qBF1Pd")
        
        for place in places[:limit]:
            name = place.text
            if name:
                results.append({"Dükkan Adı": name})

    except Exception as e:
        st.error(f"Arama sırasında teknik bir sorun oluştu: {e}")
    finally:
        driver.quit()
    
    return results

# Ana Ekran
st.title("🕵️‍♂️ Profesyonel Bölgesel Satıcı Kaşifi")
st.info("Bu araç, belirttiğiniz bölgedeki satıcıları tarayarak size listeler.")

if st.sidebar.button("Derin Taramayı Başlat"):
    if search_query and location_query:
        with st.spinner(f"Arama yapılıyor: {search_query} @ {location_query}..."):
            data = gmaps_search(search_query, location_query, target_count)
            
            if data:
                df = pd.DataFrame(data)
                st.success(f"{len(df)} dükkan bulundu!")
                st.table(df)
                
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("Excel Olarak İndir", csv, "saticilar.csv", "text/csv")
            else:
                st.warning("Sonuç bulunamadı. Lütfen aramayı farklı kelimelerle deneyin.")
    else:
        st.error("Lütfen tüm alanları doldurun.")

st.markdown("---")
st.caption("© 2025 enucuzuburda.com.tr")
