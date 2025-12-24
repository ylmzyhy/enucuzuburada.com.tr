import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Sayfa Genişliği Ayarı
st.set_page_config(page_title="Satıcı Kaşifi", layout="wide")

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
    # Standart Google Maps Arama URL'si
    search_url = f"https://www.google.com/maps/search/{query}+{location}"
    driver.get(search_url)
    time.sleep(5)

    # 1. Aşama: Daha fazla sonuç için aşağı kaydır
    try:
        scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
        for _ in range(10):
            scrollable_div.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
    except: pass

    # 2. Aşama: Linkleri Topla
    items = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    links = [item.get_attribute("href") for item in items[:limit]]

    # 3. Aşama: Her linkin içine gir ve veri ayıkla
    for link in links:
        try:
            driver.get(link)
            time.sleep(4)
            
            # İsim
            try: name = driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text
            except: name = "Bilinmiyor"

            address = "Bulunamadı"
            phone = "Bulunamadı"
            
            # Google'ın detay kutularını (Io6YTe) tara
            elements = driver.find_elements(By.CLASS_NAME, "Io6YTe")
            for el in elements:
                txt = el.text
                if not txt: continue
                
                # Telefon Kontrolü (Sayısal yoğunluk ve uzunluk)
                clean_txt = txt.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if clean_txt.startswith("+") or (clean_txt.isdigit() and len(clean_phone) > 8):
                    phone = txt
                # Adres Kontrolü (İçinde mahalle, sokak vb. geçen uzun metinler)
                elif len(txt) > 15 and any(x in txt.lower() for x in ["mah", "sok", "cad", "no:", "sk", "ist", "türkiye"]):
                    address = txt

            results.append({
                "Dükkan Adı": name,
                "Adres": address,
                "Telefon": phone,
                "Harita": link # Arka planda tutuyoruz
            })
        except: continue
    return results

# Arayüz Tasarımı
st.title("🕵️‍♂️ Profesyonel Bölgesel Satıcı Kaşifi")

with st.sidebar:
    st.header("🔍 Arama Ayarları")
    search_query = st.text_input("Ne arıyorsunuz?", "Koli Bandı")
    location_query = st.text_input("Hangi bölgede?", "İstoç")
    target_count = st.slider("Hedeflenen dükkan sayısı", 5, 50, 15)
    start_button = st.button("Derin Taramayı Başlat")

if start_button:
    if search_query and location_query:
        with st.spinner("Dükkanlar tek tek analiz ediliyor..."):
            driver = init_driver()
            data = get_details(driver, search_query, location_query, target_count)
            driver.quit()
            
            if data:
                df = pd.DataFrame(data)
                
                # --- KRİTİK DÜZELTME: LİNKİ BUTONA ÇEVİRME ---
                # Tablodaki linki tıklanabilir metin yapıyoruz
                df['Harita'] = df['Harita'].apply(lambda x: f'<a href="{x}" target="_blank">📍 Haritada Gör</a>')
                
                st.success(f"{len(df)} dükkan başarıyla listelendi!")
                
                # HTML render ederek tabloyu gösteriyoruz (Butonun çalışması için)
                st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
                
                # İndirme Butonu (Ham veri için)
                st.markdown("<br>", unsafe_allow_html=True)
                csv = pd.DataFrame(data).to_csv(index=False).encode('utf-8-sig')
                st.download_button("Excel Olarak İndir", csv, "saticilar.csv")
            else:
                st.warning("Sonuç bulunamadı.")
