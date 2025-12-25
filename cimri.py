import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. KURUMSAL GÖRÜNÜM: SAĞ ALTTAKİ YAZIYI VE MENÜYÜ GİZLE
# Sitenin en altında çıkan "Made with Streamlit" yazısını bu blok kaldırır.
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
# Logo 180px genişliğinde, sola yaslı ve arama kutularına bitişik.
col_logo, col_search, col_loc = st.columns([0.6, 2, 1])

with col_logo:
    try:
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
    fields = "formatted_phone_number,photos"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={API_KEY}&language=tr"
    res = requests.get(url).json()
    return res.get('result', {})

# 6. ARAMA BUTONU VE SONUÇLAR
if st.button("Dükkanları Bul", use_container_width=True, key="search_btn", type="primary"):
    if arama and yer:
        with st.spinner('Sonuçlar taranıyor...'):
            sonuclar = dukkan_ara(arama, yer)
            
            if sonuclar:
                st.success(f"'{yer}' bölgesinde {len(sonuclar)} yer bulundu.")
                
                for idx, dukkan in enumerate(sonuclar):
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    pid = dukkan.get('place_id')
                    
                    detay = detay_getir(pid)
                    tel = detay.get('formatted_phone_number')
                    fotolar = detay.get('photos', [])

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
                            st.subheader(isim)
                            st.write(f"📍 Adres: {adres}")
                            if tel:
                                st.write(f"📞 Telefon: {tel}")
                        
                        # BUTONLAR (Hata vermemesi için KEY değerleri sadeleştirildi)
                        b1, b2 = st.columns(2)
                        with b1:
                            harita_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}&query_place_id={pid}"
                            st.link_button("Haritada Gor", harita_link, use_container_width=True, key=f"m_{idx}")
                        
                        with b2:
                            if tel:
                                t_clean = "".join(filter(str.isdigit, tel))
                                if t_clean.startswith("0"): t_clean = "9" + t_clean
                                elif not t_clean.startswith("90"): t_clean = "90" + t_clean 
                                
                                w_url = f"https://wa.me/{t_clean}?text=Merhaba,{arama} fiyatini ogrenebilir miyim?"
                                st.link_button("WhatsApp", w_url, use_container_width=True, key=f"w_{idx}")
                            else:
                                st.button("No Yok", disabled=True, use_container_width=True, key=f"n_{idx}")
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen tüm alanları doldurun.")

st.caption("© 2025 enucuzuburada.com.tr")
