import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", layout="wide")

# 2. API ANAHTARIN
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO (Ufaltılmış ve Ortalanmış)
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    try:
        st.image("logo.png", width=120)
    except:
        st.title("En Ucuzu Burada")

# 4. FONKSİYONLAR
def dukkan_ara(urun, lokasyon):
    sorgu = f"{urun} {lokasyon}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}&key={API_KEY}&language=tr"
    try:
        response = requests.get(url).json()
        return response.get('results', [])
    except:
        return []

def telefon_bul(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number&key={API_KEY}&language=tr"
    try:
        res = requests.get(url).json()
        return res.get('result', {}).get('formatted_phone_number', '')
    except:
        return ''

# 5. ARAMA ARAYÜZÜ
st.write("---")
c1, c2 = st.columns([2, 1])
with c1:
    arama = st.text_input("Ne arıyorsunuz?", placeholder="Matkap, dübel, bant...", label_visibility="collapsed")
with c2:
    yer = st.text_input("Şehir/İlçe", value="İstoç", label_visibility="collapsed")

if st.button("Dükkanları Listele", use_container_width=True):
    if arama:
        with st.spinner('Dükkanlar getiriliyor...'):
            sonuclar = dukkan_ara(arama, yer)
            if sonuclar:
                st.success(f"{len(sonuclar)} dükkan listelendi.")
                for dukkan in sonuclar:
                    with st.container():
                        st.subheader(f"🏢 {dukkan.get('name')}")
                        st.write(f"📍 **Adres:** {dukkan.get('formatted_address')}")
                        st.write(f"⭐ **Puan:** {dukkan.get('rating', 'Yok')}")
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            map_url = f"https://www.google.com/maps/search/?api=1&query={dukkan.get('name').replace(' ', '+')}"
                            st.link_button("📍 Haritada Gör", map_url, use_container_width=True)
                        with col_btn2:
                            tel = telefon_bul(dukkan.get('place_id'))
                            if tel:
                                wa_url = f"https://wa.me/{tel.replace(' ', '').replace('+', '')}?text=Merhaba, {arama} fiyatı alabilir miyim?"
                                st.link_button("💬 WhatsApp", wa_url, use_container_width=True)
                            else:
                                st.button("📞 No Bulunamadı", disabled=True, use_container_width=True)
                        st.divider()
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen bir ürün adı yazın.")
