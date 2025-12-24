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
    time.sleep(5)

    # DAHA FAZLA SONUÇ İÇİN KAYDIRMA
    try:
        scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
        for _ in range(15): 
            scrollable_div.send_keys(Keys.PAGE_DOWN)
            time.sleep(1.5)
    except:
        pass

    # Linkleri topla - Harita linklerinin tam gelmesi için 'hfpxzc' sınıfını kullanıyoruz
    items = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    links = []
    for item in items[:limit]:
        l = item.get_attribute("href")
        if l: links.append(l)

    for link in links:
        try:
            driver.get(link)
            time.sleep(4) # Verilerin tam yüklenmesi için kritik bekleme
            
            # Dükkan İsmi
            try:
                name = driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text
            except:
                name = "Bilinmiyor"

            address = "Adres bulunamadı"
            phone = "Telefon bulunamadı"
            
            # Tüm detay butonlarını tara
            elements = driver.find_elements(By.CLASS_NAME, "Io6YTe")
            for el in elements:
                text = el.text
                if not text: continue
                
                # Telefon tespiti
                clean_phone = text.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if clean_phone.startswith("+") or (clean_phone.isdigit() and len(clean_phone) > 8):
                    phone = text
                # Adres tespiti (Şehir veya mahalle isimlerini kontrol eder)
                elif len(text) > 15 and any(kw in text.lower() for kw in ["mah", "sok", "cad", "no:", "sk.", "istanbul", "türkiye"]):
                    address = text

            results.append({
                "Dükkan Adı": name,
                "Adres": address,
                "Telefon": phone,
                "Harita Linki": link # Tam Google Maps URL'si
            })
        except:
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
        with st.spinner(f"Veriler toplanıyor... Lütfen sayfayı kapatmayın."):
            driver = init_driver()
            data = get_details(driver, search_query, location_query, target_count)
            driver.quit()
            
            if data:
                df = pd.DataFrame(data)
                st.success(f"{len(df)} dükkan bilgisi başarıyla çekildi!")
                st.dataframe(df, use_container_width=True)
                st.download_button("Excel Olarak İndir", df.to_csv(index=False).encode('utf-8-sig'), "saticilar_liste.csv")
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen alanları doldurun.")
