import streamlit as st
import requests

# 1. TEMEL AYARLAR
st.set_page_config(page_title="En Ucuzu Burada", layout="centered")

# 2. LOGO (Ufaltılmış)
try:
    st.image("logo.png", width=120)
except:
    st.title("🛒 En Ucuzu Burada")

# 3. API ANAHTARI
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 4. FONKSİYONLAR
def dukkan_getir(urun, yer):
    sorgu = f"{urun} {yer}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}&key={API_KEY}&language=tr"
    try:
        r = requests.get(url).json()
        return r.get("results", [])
    except:
        return []

# 5. ARAYÜZ
st.write("---")
arama = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Matkap, Vida...")
lokasyon = st.text_input("Nerede?", value="İstoç")

if st.button("Dükkanları Bul"):
    if arama:
        sonuclar = dukkan_getir(arama, lokasyon)
        if sonuclar:
            st.success(f"{len(sonuclar)} dükkan bulundu!")
            for dukkan in sonuclar:
                st.subheader(f"🏢 {dukkan.get('name')}")
                st.write(f"📍 {dukkan.get('formatted_address')}")
                st.write(f"⭐ Puan: {dukkan.get('rating', 'Yok')}")
                
                # Harita Linki
                id_ = dukkan.get('place_id')
                link = f"https://www.google.com/maps/search/?api=1&query=Google&query_place_id={id_}"
                st.link_button("📍 Konumu Gör", link)
                st.divider()
        else:
            st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen bir ürün ismi girin.")
