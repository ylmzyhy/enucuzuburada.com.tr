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
    options.add_argument("--headless")  # Sunucu için zorunlu
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    # Streamlit Cloud üzerindeki Chromium yolu
    options.binary_location = "/usr/bin/chromium"
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def gmaps_search(query, location, limit):
    driver = init_driver()
    results = []
    
    try:
        full_query = f"https://www.google.com/maps/search/{query}+{location}"
        driver.get(full_query)
        
        # Sonuçların yüklenmesini bekle
        wait = WebDriverWait(driver, 10)
        
        # Kaydırma işlemi (Scroll) - Daha fazla sonuç yüklemek için
        scrollable_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']")))
        
        last_count = 0
        while len(results) < limit:
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(2)
            
            # Dükkan kartlarını bul
            places = driver.find_elements(By.CSS_SELECTOR, "div.Nv2Ybe") 
            
            for place in places[last_count:]:
                try:
                    name = place.find_element(By.CSS_SELECTOR, "div.fontHeadlineSmall").text
                    try:
                        rating = place.find_element(By.CSS_SELECTOR, "span.MW4etd").text
                    except:
                        rating = "N/A"
                    
                    results.append({"Dükkan Adı": name, "Puan": rating})
                    
                    if len(results) >= limit:
                        break
                except:
                    continue
            
            if len(places) == last_count: # Daha fazla sonuç yüklenmiyorsa dur
                break
            last_count = len(places)

    except Exception as e:
        st.error(f"Arama sırasında bir hata oluştu: {e}")
    finally:
        driver.quit()
    
    return results

# Ana Ekran
st.title("🕵️‍♂️ Profesyonel Bölgesel Satıcı Kaşifi")
st.info("Bu araç, belirttiğiniz bölgedeki satıcıları Google Haritalar üzerinden tarayarak size listeler.")

if st.sidebar.button("Derin Taramayı Başlat"):
    if search_query and location_query:
        with st.spinner(f"{location_query} bölgesinde {search_query} satıcıları aranıyor..."):
            data = gmaps_search(search_query, location_query, target_count)
            
            if data:
                df = pd.DataFrame(data)
                st.success(f"{len(df)} adet dükkan bulundu!")
                st.table(df)
                
                # CSV İndirme Butonu
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("Sonuçları Excel (CSV) Olarak İndir", csv, "saticilar.csv", "text/csv")
            else:
                st.warning("Hiç sonuç bulunamadı. Lütfen aramayı daraltın veya farklı anahtar kelimeler deneyin.")
    else:
        st.error("Lütfen hem ürün hem de bölge kısmını doldurun.")

# Alt Bilgi
st.markdown("---")
st.caption("© 2025 enucuzuburda.com.tr - Tüm hakları saklıdır.")
