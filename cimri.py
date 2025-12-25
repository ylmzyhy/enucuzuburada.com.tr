import streamlit as st

# 1. Sayfa Ayarları (Sekme ismi ve ikonu)
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. Logo Ekleme (Dosya adın neyse onu yazıyoruz, .png olarak güncelledim)
try:
    st.image("logo.png", width=250)
except:
    st.warning("Logo dosyası henüz GitHub'a yüklenmemiş görünüyor.")

# 3. Renk ve Buton Stilleri (Logonla uyumlu olması için)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #f39233; /* Logonun Turuncusu */
        color: white;
        border-radius: 5px;
        font-weight: bold;
    }
    h1 {
        color: #38b2ac; /* Logonun Turkuazı */
    }
    </style>
    """, unsafe_allow_all_html=True)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

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
    search_url = f"https://www.google.com/maps/search/{query}+{location}"
    driver.get(search_url)
    time.sleep(5)

    # Sonuçları yüklemek için kaydır
    try:
        scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
        for _ in range(8):
            scrollable_div.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
    except: pass

    items = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    links = [item.get_attribute("href") for item in items[:limit]]

    for link in links:
        try:
            driver.get(link)
            time.sleep(4)
            
            try: name = driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text
            except: name = "Bilinmiyor"

            address = "Adres bulunamadı"
            phone = "Telefon bulunamadı"
            
            # NOKTA ATIŞI: Adres ve Telefon çekme (Google'ın buton etiketlerini kullanıyoruz)
            try:
                # Adres butonu genellikle 'Adres: ...' diye bir aria-label içerir
                addr_element = driver.find_element(By.CSS_SELECTOR, "[data-item-id='address']")
                address = addr_element.get_attribute("aria-label").replace("Adres: ", "")
            except:
                # Yedek adres bulucu (Plus Code olmayan en uzun metni seçer)
                elements = driver.find_elements(By.CLASS_NAME, "Io6YTe")
                for el in elements:
                    txt = el.text
                    if len(txt) > 25 and "+" not in txt:
                        address = txt
                        break

            try:
                # Telefon butonu 'Telefon: ...' şeklinde bir aria-label içerir
                phone_element = driver.find_element(By.CSS_SELECTOR, "[data-tooltip='Telefon numarasını kopyalayın']")
                phone = phone_element.get_attribute("aria-label").replace("Telefon: ", "")
            except:
                # Yedek telefon bulucu
                elements = driver.find_elements(By.CLASS_NAME, "Io6YTe")
                for el in elements:
                    txt = el.text.replace(" ", "")
                    if (txt.startswith("0") or txt.startswith("+")) and len(txt) > 9:
                        phone = el.text
                        break

            results.append({
                "Dükkan Adı": name,
                "Adres": address,
                "Telefon": phone,
                "Harita": link
            })
        except: continue
    return results

# Arayüz
st.title("🕵️‍♂️ Profesyonel Bölgesel Satıcı Kaşifi")

with st.sidebar:
    st.header("🔍 Arama Ayarları")
    search_query = st.text_input("Ne arıyorsunuz?", "Koli Bandı")
    location_query = st.text_input("Hangi bölgede?", "İstoç")
    target_count = st.slider("Hedeflenen dükkan sayısı", 5, 50, 10)
    start_button = st.button("Derin Taramayı Başlat")

if start_button:
    if search_query and location_query:
        with st.spinner("Dükkan detayları analiz ediliyor..."):
            driver = init_driver()
            data = get_details(driver, search_query, location_query, target_count)
            driver.quit()
            
            if data:
                df = pd.DataFrame(data)
                
                # Görsel düzenlemeler
                df_display = df.copy()
                df_display['Harita'] = df_display['Harita'].apply(lambda x: f'<a href="{x}" target="_blank">📍 Haritada Gör</a>')
                
                st.success(f"{len(df)} dükkan başarıyla listelendi!")
                st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("Sonuçları Excel Olarak İndir", csv, "saticilar_listesi.csv")
            else:
                st.warning("Sonuç bulunamadı.")

