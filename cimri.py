import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. KURUMSAL GÖRÜNÜM İÇİN MENÜLERİ GİZLEME (CSS)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. API ANAHTARI
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 4. LOGO VE ARAMA ALANI (SOLDA VE YAKIN)
col_logo, col_search, col_loc = st.columns([0.6, 2, 1])

with col_logo:
    try:
        # Logo genişliği 180px, sola yaslı
        st.image("logo.png", width=180)
    except:
        st.subheader("🛒")

with col_search:
    arama = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Kaynak Makinesi, Matkap...", key="main_search")

with col_loc:
    yer = st.text_input("Şehir / İlçe seçin", placeholder="Örn: Ankara Ostim...", key="main_loc")

# 5. FONKSİYONLAR
def dukkan_ara(urun, lokasyon):
    sorgu = f"{urun} {lokasyon}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}&key={API_KEY}&language=tr"
    response = requests.get(url).json()
    return response.get('results', [])

def detay_getir(place_id):
    fields = "formatted_phone_number,opening_hours,international_phone_number,photos"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={API_KEY}&language=tr"
    res = requests.get(url).json()
    return res.get('result', {})

# 6. ARAMA BUTONU VE SONUÇLAR
if st.button("Dükkanları ve Fiyat Sorulacak Yerleri Bul", use_container_width=True, key="search_btn"):
    if arama and yer:
        with st.spinner('Detaylı bilgiler çekiliyor...'):
            sonuclar = dukkan_ara(arama, yer)
            
            if sonuclar:
                st.success(f"'{yer}' bölgesinde {len(sonuclar)} yer bulundu.")
                
                for idx, dukkan in enumerate(sonuclar):
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    pid = dukkan.get('place_id')
                    
                    detay = detay_getir(pid)
                    tel = detay.get('formatted_phone_number') or detay.get('international_phone_number')
                    saatler = detay.get('opening_hours', {})
                    fotolar = detay.get('photos', [])
                    
                    acik_mi_text = "Bilgi Yok"
                    if saatler:
                        acik_mi_text = "✅ ŞİMDİ AÇIK" if saatler.get('open_now') else "❌ ŞİMDİ KAPALI"

                    with st.container():
                        st.divider()
                        col_img, col_txt = st.columns([1, 3])
                        
                        with col_img:
                            if fotolar:
                                foto_ref = fotolar[0].get('photo_reference')
                                foto_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={foto_ref}&key={API_KEY}"
                                st.image(foto_url, use_container_width=True)
                            else:
                                st.write("🖼️ Fotoğraf Yok")

                        with col_txt:
                            st.subheader(f"🏢 {isim}")
                            st.write(f"📍 **Adres:** {adres}")
                            if tel:
                                st.write(f"📞 **Telefon:** {tel}")
                            st.write(f"⏰ {acik_mi_text}")
                        
                        b1, b2 = st.columns(2)
                        with b1:
                            harita_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}&query_place_id={pid}"
                            st.link_button("📍 Konum", harita_link, use_container_width=True, key=f"m_{idx}_{pid}")
                        
                        with b2:
                            if tel:
                                temiz_tel = "".join(filter(str.isdigit, tel))
                                if temiz_tel.startswith("0"): temiz_tel = "9" + temiz_tel
                                elif not temiz_tel.startswith("90"): temiz_tel = "90" + temiz_tel 
                                
                                wa_mesaj = f"Merhaba, {arama} ürünü için fiyat bilgisi alabilir miyim?"
                                wa_link = f"https://wa.me/{temiz_tel}?text={wa_mesaj}"
                                st.link_button("💬 WhatsApp", wa_link, type="primary", use_container_width=True, key=f"w_{idx}_{pid}")
                            else:
                                st.button("📞 No Mevcut Değil", disabled=True, use_container_width=True, key=f"n_{idx}_{pid}")
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen alanları doldurun.")

st.caption("© 2025 enucuzuburada.com.tr")
