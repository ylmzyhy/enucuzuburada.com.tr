import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARIN
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO VE ÜST KISIM
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.title("🛒 En Ucuzu Burada")

# 4. FONKSİYONLAR
def dukkan_ara(kelime):
    # İstoç odaklı arama yapar
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={kelime}+istoç+istanbul&key={API_KEY}&language=tr"
    response = requests.get(url).json()
    return response.get('results', [])

def telefon_bul(place_id):
    # Dükkanın telefonunu almak için detay sorgusu yapar
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number&key={API_KEY}&language=tr"
    res = requests.get(url).json()
    return res.get('result', {}).get('formatted_phone_number', '')

# 5. ARAYÜZ
st.write("---")
arama = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Dübel, Bant, Vida...")

if st.button("Dükkanları Bul"):
    if arama:
        with st.spinner('Gerçek zamanlı veriler taranıyor...'):
            sonuclar = dukkan_ara(arama)
            if sonuclar:
                st.success(f"'{arama}' için {len(sonuclar)} dükkan bulundu.")
                for dukkan in sonuclar:
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    puan = dukkan.get('rating', 'Yok')
                    place_id = dukkan.get('place_id')
                    
                    # Kart Tasarımı
                    with st.container():
                        st.subheader(f"🏢 {isim}")
                        st.write(f"📍 **Adres:** {adres}")
                        st.write(f"⭐ **Puan:** {puan}")
                        
                        # Butonlar için sütunlar
                        c1, c2 = st.columns(2)
                        with c1:
                            harita_url = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}&query_place_id={place_id}"
                            st.link_button("📍 Haritada Gör", harita_url, use_container_width=True)
                        with c2:
                            # Telefonu bulup WhatsApp'a bağla
                            tel = telefon_bul(place_id)
                            wa_msg = f"Merhaba, {arama} fiyatını öğrenmek istiyorum."
                            if tel:
                                wa_link = f"https://wa.me/{tel.replace(' ', '').replace('+', '')}?text={wa_msg}"
                                st.link_button("💬 WhatsApp'tan Sor", wa_link, type="primary", use_container_width=True)
                            else:
                                st.write("📞 Telefon bulunamadı")
                        st.divider()
            else:
                st.warning("Üzgünüz, dükkan bulunamadı.")
    else:
        st.error("Lütfen bir ürün adı yazın.")

st.caption("© 2025 enucuzuburada.com.tr | İstoç Rehberi")
