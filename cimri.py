import streamlit as st
import requests

# 1. SAYFA AYARLARI (Hata almamak için mutlaka en üstte)
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARIN (Görselden aldım)
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO VE BAŞLIK
try:
    # Logonun ortalı durması için sütun kullanıyoruz
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image("logo.png", width=300)
except:
    st.title("En Ucuzu Burada")

# 4. TASARIM (Hata riskini sıfırlamak için en sade hal)
st.markdown("""
<style>
    .dukkan-kart {
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        background-color: #f9f9f9;
    }
    .stButton>button {
        background-color: #f39233 !important;
        color: white !important;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_all_html=True)

st.subheader("İstoç ve Çevresinde En Ucuzunu Bul")

# 5. ARAMA FONKSİYONU
def veri_getir(kelime):
    # İstoç odaklı arama
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={kelime}+istoç&key={API_KEY}&language=tr"
    response = requests.get(url).json()
    return response.get('results', [])

# 6. KULLANICI ARAYÜZÜ
arama = st.text_input("", placeholder="Örn: Dübel, Bant, Koli...")

if st.button("Hemen Ara"):
    if arama:
        with st.spinner('Gerçek zamanlı dükkanlar listeleniyor...'):
            sonuclar = veri_getir(arama)
            
            if sonuclar:
                st.success(f"'{arama}' için {len(sonuclar)} dükkan bulundu.")
                for dukkan in sonuclar:
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    puan = dukkan.get('rating', 'Yok')
                    
                    # Dükkan Kartı
                    st.markdown(f"""
                    <div class="dukkan-kart">
                        <h4>🏢 {isim}</h4>
                        <p>📍 {adres}</p>
                        <p>⭐ Puan: {puan}</p>
                    </div>
                    """, unsafe_allow_all_html=True)
                    
                    # Butonlar
                    col1, col2 = st.columns(2)
                    with col1:
                        harita_url = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}"
                        st.markdown(f"[📍 Haritada Gör]({harita_url})")
                    with col2:
                        wa_mesaj = f"Merhaba, {arama} fiyatını öğrenebilir miyim?"
                        st.markdown(f"[💬 WhatsApp'tan Sor](https://wa.me/?text={wa_mesaj})")
                    st.divider()
            else:
                st.error("Dükkan bulunamadı. Lütfen kelimeyi kontrol edin.")
    else:
        st.warning("Lütfen bir ürün ismi girin.")

st.markdown("---")
st.write("enucuzuburada.com.tr | 2025")
