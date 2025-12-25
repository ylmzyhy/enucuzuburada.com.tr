import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARI
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO VE ARAMA ALANI (BOŞLUKSUZ VE YAKIN)
# Logoyu küçük tutmak ve arama kutusuna yaklaştırmak için dar bir sütun yapısı
col_logo, col_search, col_loc = st.columns([0.5, 2, 1], gap="small")

with col_logo:
    try:
        # Logo genişliği 150px yapılarak küçültüldü ve arama kutusuna yaklaştırıldı
        st.image("logo.png", width=150)
    except:
        st.subheader("🛒")

with col_search:
    arama = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Matkap, Kaynak Makinesi...", key="search_input")

with col_loc:
    yer = st.text_input("Şehir / İlçe", placeholder="Örn: Ostim, İkitelli...", key="loc_input")

# 4. FONKSİYONLAR
def dukkan_ara(u, l):
    s = f"{u} {l}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={s}&key={API_KEY}&language=tr"
    return requests.get(url).json().get('results', [])

def detay_getir(pid):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={pid}&fields=formatted_phone_number,photos&key={API_KEY}&language=tr"
    return requests.get(url).json().get('result', {})

# 5. ARAMA BUTONU VE SONUÇLAR
if st.button("Dükkanları Bul", use_container_width=True, type="primary", key="btn_main"):
    if arama and yer:
        with st.spinner('Taranıyor...'):
            sonuclar = dukkan_ara(arama, yer)
            if sonuclar:
                st.success(f"{len(sonuclar)} yer bulundu.")
                for i, d in enumerate(sonuclar):
                    pid = d.get('place_id')
                    isim = d.get('name', 'İşletme')
                    adres = d.get('formatted_address', 'Adres yok')
                    
                    detay = detay_getir(pid)
                    tel = detay.get('formatted_phone_number')
                    fotolar = detay.get('photos', [])

                    # DÜKKAN KARTI (Bozulmayan Sade Yapı)
                    with st.container(border=True):
                        c_img, c_txt = st.columns([1, 3])
                        with c_img:
                            if fotolar:
                                f_ref = fotolar[0].get('photo_reference')
                                f_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=300&photoreference={f_ref}&key={API_KEY}"
                                st.image(f_url, use_container_width=True)
                            else:
                                st.write("🖼️ Foto Yok")
                        
                        with c_txt:
                            st.subheader(isim)
                            st.write(f"Adres: {adres}")
                            if tel: st.write(f"Tel: {tel}")
                        
                        # BUTONLAR (Hata riskine karşı emojisiz ve basit key yapısı)
                        b1, b2 = st.columns(2)
                        with b1:
                            m_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ','+')}&query_place_id={pid}"
                            st.link_button("Haritada Gor", m_link, use_container_width=True, key=f"m_{i}")
                        with b2:
                            if tel:
                                t_clean = "".join(filter(str.isdigit, tel))
                                if t_clean.startswith("0"): t_clean = "9" + t_clean
                                elif not t_clean.startswith("90"): t_clean = "90" + t_clean
                                w_link = f"https://wa.me/{t_clean}?text=Merhaba,{arama} fiyatini ogrenebilir miyim?"
                                st.link_button("WhatsApp", w_link, use_container_width=True, key=f"w_{i}")
                            else:
                                st.button("Telefon Yok", disabled=True, use_container_width=True, key=f"n_{i}")
            else:
                st.warning("Sonuç yok.")
    else:
        st.error("Lütfen alanları doldurun.")

st.caption("© 2025 enucuzuburada.com.tr")
