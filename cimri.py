from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
# Sunucudaki Chromium'un yerini tam olarak gösteriyoruz:
options.binary_location = "/usr/bin/chromium" 

# Sürücüyü bu ayarlar ve Service kullanarak başlatıyoruz:
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Sayfa Yapılandırması
st.set_page_config(page_title="Piyasa Dedektifi v5", layout="wide")
st.title("🕵️‍♂️ Profesyonel Bölgesel Satıcı Kaşifi")

with st.sidebar:
    st.header("Arama Ayarları")
    urun = st.text_input("Ne arıyorsunuz?", "Koli Bandı")
    bolge = st.text_input("Hangi bölgede?", "İstoç")
    limit = st.slider("Hedeflenen dükkan sayısı", 5, 40, 15)
    ara_butonu = st.button("Derin Taramayı Başlat")

if ara_butonu:
    with st.spinner(f'{limit} adet dükkan için harita derinleştiriliyor...'):
        options = Options()
        options.add_argument("--headless") 
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--lang=tr")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        try:
            sorgu = f"{bolge} {urun} mağazası"
            url = f"http://www.google.com/maps/search/{sorgu.replace(' ', '+')}"
            driver.get(url)
            time.sleep(5)
            
            # --- GELİŞMİŞ SCROLL (Listenin derinlerine inme) ---
            try:
                scroll_panel = driver.find_element(By.XPATH, '//div[@role="feed"]')
                last_height = 0
                while len(driver.find_elements(By.CLASS_NAME, "hfpxzc")) < limit:
                    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_panel)
                    time.sleep(2)
                    new_height = driver.execute_script('return arguments[0].scrollHeight', scroll_panel)
                    if new_height == last_height: break
                    last_height = new_height
            except: pass

            sonuclar = []
            kartlar = driver.find_elements(By.CLASS_NAME, "hfpxzc")
            
            pbar = st.progress(0)
            for i, kart in enumerate(kartlar[:limit]):
                try:
                    isim = kart.get_attribute("aria-label")
                    driver.execute_script("arguments[0].click();", kart)
                    time.sleep(3)
                    
                    # Koordinat Ayıklama
                    current_url = driver.current_url
                    koordinat = None
                    google_maps_link = None
                    match = re.search(r'@([\d\.]+),([\d\.]+)', current_url)
                    
                    if match:
                        lat, lon = match.group(1), match.group(2)
                        koordinat = {"lat": float(lat), "lon": float(lon)}
                        google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
                    
                    # Diğer Bilgiler
                    adres = "Yok"
                    telefon = "Yok"
                    try: adres = driver.find_element(By.CSS_SELECTOR, "[data-item-id='address']").text
                    except: pass
                    try: telefon = driver.find_element(By.CSS_SELECTOR, "[data-item-id*='phone:tel:']").text
                    except: pass
                    
                    sonuclar.append({
                        "Dükkan Adı": isim,
                        "Telefon": telefon,
                        "Adres": adres,
                        "Konum Linki": google_maps_link, # Tıklanabilir link
                        "coords": koordinat # Harita çizimi için gizli veri
                    })
                    pbar.progress((i + 1) / len(kartlar[:limit]))
                except: continue

            if sonuclar:
                df = pd.DataFrame(sonuclar)
                st.success(f"{len(sonuclar)} dükkan başarıyla listelendi.")
                
                # --- TABLO GÖSTERİMİ ---
                st.subheader("📋 Satıcı Detayları")
                # Harita koordinatlarını içeren teknik 'coords' sütununu tabloda göstermiyoruz
                tablo_df = df.drop(columns=["coords"])
                
                st.dataframe(
                    tablo_df,
                    column_config={
                        "Konum Linki": st.column_config.LinkColumn(
                            "Harita",
                            display_text="📍 Konuma Git" # Kullanıcı sadece bu yazıyı görecek
                        ),
                    },
                    use_container_width=True,
                    hide_index=True
                )
                
                # --- GÖRSEL HARİTA ---
                st.divider()
                st.subheader("📍 Dükkanların Bölgesel Dağılımı")
                map_df = pd.DataFrame([s["coords"] for s in sonuclar if s["coords"] is not None])
                if not map_df.empty:
                    st.map(map_df)
                
                # İndirme Butonu
                csv = df.drop(columns=["coords"]).to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 Listeyi Excel Olarak İndir", csv, "saticilar.csv", "text/csv")
            
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
        finally:

            driver.quit()
