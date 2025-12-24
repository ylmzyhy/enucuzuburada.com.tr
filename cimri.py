import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

st.set_page_config(page_title="En Ucuzu Burada - Profesyonel Tarayıcı", layout="wide")

def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/usr/bin/chromium"
    service = Service("/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)

def get_details(driver, query, location, limit):
    results = []
    search_url = f"https://www.google.com/maps/search/{query}+{location}"
    driver.get(search_url)
    time.sleep(6) # İlk yükleme için uzun bekleme

    # SONUÇ SAYISINI ARTIRMAK İÇİN KAYDIRMA (SCROLL)
    scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
    for _ in range(8): # Daha fazla kaydırarak daha çok sonuç yüklemesini sağlıyoruz
        scrollable_div.send_keys(Keys.PAGE_DOWN)
        time.sleep(1.5)

    # Linkleri topla
    items = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    links = [item.get_attribute("href") for item in items[:limit]]

    for link in links:
        try:
            driver.get(link)
            time.sleep(4) # Verilerin yüklenmesi için kritik bekleme süresi
            
            # İsim Çekme
            try:
                name = driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text
            except:
                name = "Bilinmiyor"

            # ADRES VE TELEFON İÇİN GENEL TARAMA
            # Google'ın buton yapıları değişse bile metinden yakalama
            address = "Adres bulunamadı"
            phone = "Telefon bulunamadı"
            
            elements = driver.find_elements(By.CLASS_NAME, "Io6YTe") # Google'ın tüm detay satırları
            for el in elements:
                text = el.text
                if "+" in text or (text.replace(" ", "").isdigit() and len(text) > 8): # Telefon tespiti
                    phone = text
                elif len(text) > 20 and any(char.isdigit() for char in text): # Adres tespiti
                    address = text

            results.append({
                "Dükkan Adı": name,
                "Adres": address,
                "Telefon": phone,
                "Harita Linki": link
            })
        except Exception as e:
            continue
    return results

# Arayüz
st.title("🕵️‍♂️ Profesyonel Bölgesel Satıcı Kaşifi")
st.sidebar.header("🔍 Arama Ayarları")
search_query = st.sidebar.text_input("Ne arıyorsunuz?", "Koli Bandı")
location_query = st.sidebar.text_input("Hangi bölgede?", "İstoç")
target_count = st.sidebar.slider("Hedeflenen dükkan sayısı", 5, 50, 15)

if st.sidebar.button("Derin Taramayı Başlat"):
    if search_query and location_query:
        with st.spinner("Detaylı veriler çekiliyor (Her dükkan için yaklaşık 5 saniye sürer)..."):
            driver = init_driver()
            data = get_details(driver, search_query, location_query, target_count)
            driver.quit()
            
            if data:
                df = pd.DataFrame(data)
                st.success(f"{len(df)} dükkan başarıyla listelendi!")
                st.dataframe(df, use_container_width=True)
                
                # Excel/CSV İndirme
                st.download_button("Sonuçları Excel Olarak İndir", df.to_csv(index=False).encode('utf-8-sig'), "saticilar_liste.csv")
            else:
                st.warning("Sonuç bulunamadı.")
