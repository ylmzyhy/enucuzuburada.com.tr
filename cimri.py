import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Sayfa Ayarları
st.set_page_config(page_title="En Ucuzu Burada - Detaylı Satıcı Kaşifi", layout="wide")

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
    # Arama URL'si
    search_url = f"https://www.google.com/maps/search/{query}+{location}"
    driver.get(search_url)
    time.sleep(5)

    # Sayfayı aşağı kaydırarak tüm sonuçları yükle
    scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
    for _ in range(5): # Limit arttıkça bu sayı artırılabilir
        scrollable_div.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    # Dükkan linklerini topla
    items = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    links = [item.get_attribute("href") for item in items[:limit]]

    for link in links:
        try:
            driver.get(link)
            time.sleep(3)
            
            name = driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text
            
            # Adres ve Telefonu belirli simgelere göre bulalım
            try:
                address = driver.find_element(By.CSS_SELECTOR, "button[data-item-id='address']").get_attribute("aria-label").replace("Adres: ", "")
            except:
                address = "Adres bulunamadı"
                
            try:
                phone = driver.find_element(By.CSS_SELECTOR, "button[data-tooltip='Telefon numarasını kopyalayın']").get_attribute("aria-label").replace("Telefon: ", "")
            except:
                phone = "Telefon bulunamadı"

            results.append({
                "Dükkan Adı": name,
                "Adres": address,
                "Telefon": phone,
                "Harita Linki": link
            })
        except:
            continue
    return results

# Arayüz
st.title("🕵️‍♂️ Profesyonel Bölgesel Satıcı Kaşifi")
st.sidebar.header("🔍 Arama Ayarları")
search_query = st.sidebar.text_input("Ne arıyorsunuz?", "Koli Bandı")
location_query = st.sidebar.text_input("Hangi bölgede?", "İstoç")
target_count = st.sidebar.slider("Hedeflenen dükkan sayısı", 5, 30, 15)

if st.sidebar.button("Derin Taramayı Başlat"):
    if search_query and location_query:
        with st.spinner("Her dükkanın detayları tek tek analiz ediliyor, lütfen bekleyin..."):
            driver = init_driver()
            data = get_details(driver, search_query, location_query, target_count)
            driver.quit()
            
            if data:
                df = pd.DataFrame(data)
                st.success(f"{len(df)} dükkan bilgisi tüm detaylarıyla çekildi!")
                st.dataframe(df, use_container_width=True)
                st.download_button("Excel Olarak İndir", df.to_csv(index=False).encode('utf-8-sig'), "detayli_saticilar.csv")
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen alanları doldurun.")
