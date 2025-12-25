import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. KURUMSAL GÖRÜNÜM: SAĞ ALTTAKİ YAZIYI VE MENÜYÜ GİZLE
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 3. API ANAHTARI
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 4. LOGO VE ARAMA ALANI (SOLDA VE YAKIN)
# Sütun oranları logoyu küçük (180px) tutup kutulara yaklaştırır
col_logo, col_search, col_loc = st.columns([0.6, 2, 1])

with col_logo:
    try:
        st.image("logo.png", width=180)
    except:
        st.subheader("🛒")

with col_search:
    arama = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Kaynak Makinesi...", key="search_q")

with col_loc:
    yer = st.text_input("Şehir / İlçe", placeholder="Örn: Ostim...", key="loc_q")

# 5. FONKSİYONLAR
def dukkan_ara(urun, lokasyon):
    sorgu = f"{urun} {lokasyon}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}&key={API_KEY}&language=tr"
    return requests.get(url).json().get('results', [])

def detay_getir(pid):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={pid}&fields=formatted_phone_number,photos&key={API_KEY}&language=tr"
    return requests.get(url).json().get('result', {})

# 6. ARAMA BUTONU VE SONUÇLAR
if st.button("Dükkanları Bul", use_container_width=True, type="primary", key="main_search_btn"):
    if arama and yer:
        with st.spinner('Taranıyor...'):
            sonuclar = dukkan_ara(arama, yer)
            if sonuclar:
                for idx, dukkan in enumerate(sonuclar):
                    pid = dukkan.get('place_id')
                    isim = dukkan.get('name', 'İşletme')
                    adres = dukkan.get('formatted_address', 'Adres yok')
                    
                    detay = detay_getir(pid)
                    tel = detay.get('formatted_phone_number')
                    fotolar = detay.get('photos', [])

                    # DÜKKAN KARTI
                    with st.container():
                        st.divider()
                        c_img, c_txt = st.columns([1, 3])
                        with c_img:
                            if fotolar:
                                f_ref = fotolar[0].get('photo_reference')
                                f_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={f_ref}&key={API_KEY}"
                                st.image(f_url, use_container_width=True)
                            else:
                                st.write("🖼️ Fotoğraf Yok")
                        
                        with c_txt:
                            st.subheader(isim)
                            st.write(f"Adres: {adres}")
                            if tel: st.write(f"Telefon: {tel}")
                        
                        # BUTONLAR (HATA VERMEYEN EN SADE YAPI)
                        b1, b2 = st.columns(2)
                        with b1:
                            m_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ','+')}&query_place_id={pid}"
                            # Emojileri sildik, key'leri en sade hale getirdik (m_0, m_1...)
                            st.link_button("Haritada Gor", m_link, use_container_width=True, key=f"m_{idx}")
                        with b2:
                            if tel:
                                t_clean = "".join(filter(str.isdigit, tel))
                                if t_clean.startswith("0"): t_clean = "9" + t_clean
                                elif not t_clean.startswith("90"): t_clean = "90" + t_clean
                                w_link = f"https://wa.me/{t_clean}?text=Merhaba,{arama} fiyatini ogrenebilir miyim?"
                                st.link_button("WhatsApp", w_link, use_container_width=True, key=f"w_{idx}")
                            else:
                                st.button("No Yok", disabled=True, use_container_width=True, key=f"n_{idx}")
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen alanları doldurun.")

st.caption("© 2025 enucuzuburada.com.tr")
