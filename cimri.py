import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", layout="wide")

# 2. API ANAHTARIN (Görüntüden aldım)
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO
try:
    st.image("logo.png", width=250)
except:
    st.write("Logo Yükleniyor...")

# 4. TASARIM (Görselliği iyileştirmek için)
st.markdown("""
<style>
    .result-card {
        border: 1px solid #e6e9ef;
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .stButton>button {
        background-color: #f39233 !important;
        color: white !important;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_all_html=True)

st.title("En Ucuzu Burada")
st.subheader("Aradığın ürün için İstoç dükkanlarını bul")

# 5. ARAMA FONKSİYONU (Google Maps'e Bağlanır)
def dukkan_ara(kelime):
    # İstoç ve çevresinde arama yapar
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={kelime}+istoç&key={API_KEY}&language=tr"
    response = requests.get(url).json()
    return response.get('results', [])

# 6. KULLANICI ARAYÜZÜ
arama = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Bant, Dübel, Boya...")

if st.button("Ara"):
    if arama:
        with st.spinner('Gerçek zamanlı veriler çekiliyor...'):
            sonuclar = dukkan_ara(arama)
            
            if sonuclar:
                st.success(f"'{arama}' için {len(sonuclar)} dükkan bulundu!")
                
                for dukkan in sonuclar:
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    puan = dukkan.get('rating', 'Yok')
                    place_id = dukkan.get('place_id')
                    harita_linki = f"https://www.google.com/maps/search/?api=1&query={isim}&query_place_id={place_id}"
                    
                    # Dükkan Kartı Tasarımı
                    with st.container():
                        st.markdown(f"""
                        <div class="result-card">
                            <h4>🏢 {isim}</h4>
                            <p>📍 <b>Adres:</b> {adres}</p>
                            <p>⭐ <b>Puan:</b> {puan}</p>
                        </div>
                        """, unsafe_allow_all_html=True)
                        
                        # Harita ve WhatsApp butonları
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown(f'<a href="{harita_linki}" target="_blank"><button style="width:100%; cursor:pointer; padding:10px; background-color:#38b2ac; color:white; border:none; border-radius:5px;">📍 Haritada Gör</button></a>', unsafe_allow_all_html=True)
                        with c2:
                            # WhatsApp mesajı hazırlama
                            wa_mesaj = f"Merhaba, {arama} fiyatını öğrenebilir miyim?"
                            wa_link = f"https://wa.me/?text={wa_mesaj}"
                            st.markdown(f'<a href="{wa_link}" target="_blank"><button style="width:100%; cursor:pointer; padding:10px; background-color:#25D366; color:white; border:none; border-radius:5px;">💬 Fiyat Sor</button></a>', unsafe_allow_all_html=True)
                        st.write("") # Boşluk
            else:
                st.error("Üzgünüz, bu ürün için bir dükkan bulunamadı.")
    else:
        st.warning("Lütfen bir ürün ismi yazın.")

# 7. FOOTER
st.markdown("---")
st.write("enucuzuburada.com.tr | 2025")
