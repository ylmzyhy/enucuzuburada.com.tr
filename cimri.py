import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", layout="wide")

# 2. GOOGLE API ANAHTARIN (Resminde görünen anahtar)
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO
try:
    st.image("logo.png", width=250)
except:
    st.title("🛒 En Ucuzu Burada")

# 4. GOOGLE MAPS ARAMA FONKSİYONU (Hata tespiti için güncellendi)
def dukkan_getir(sorgu):
    # İstoç kelimesini sorguya ekliyoruz
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}+istoç+istanbul&key={API_KEY}&language=tr"
    response = requests.get(url).json()
    
    # Ekranda hata analizi yapmamızı sağlar
    if response.get("status") != "OK" and response.get("status") != "ZERO_RESULTS":
        st.error(f"Google API Mesajı: {response.get('status')}")
        if response.get("error_message"):
            st.info(f"Detay: {response.get('error_message')}")
            
    return response.get('results', [])

# 5. ARAYÜZ
st.write("---")
arama_terimi = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Dübel, Bant, Koli...")

if st.button("Dükkanları Bul"):
    if arama_terimi:
        with st.spinner('İstoç dükkanları taranıyor...'):
            sonuclar = dukkan_getir(arama_terimi)
            
            if sonuclar:
                st.success(f"'{arama_terimi}' için {len(sonuclar)} dükkan bulundu.")
                for dukkan in sonuclar:
                    with st.container():
                        st.subheader(f"🏢 {dukkan.get('name')}")
                        st.write(f"📍 **Adres:** {dukkan.get('formatted_address')}")
                        st.write(f"⭐ **Puan:** {dukkan.get('rating', 'Yok')}")
                        st.divider()
            else:
                st.warning("Bu ürün için şu an bir dükkan listelenemedi. Google anahtarınızın aktifleşmesini bekliyor olabiliriz.")
    else:
        st.error("Lütfen bir ürün adı yazın.")

st.caption("© 2025 enucuzuburada.com.tr")
