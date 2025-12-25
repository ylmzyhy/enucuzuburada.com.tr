import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. LOGO GÖRÜNTÜLEME
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.header("En Ucuzu Burada")

# 3. TASARIM (CSS)
st.markdown("""
<style>
    .result-card {
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 12px;
        background-color: #fcfcfc;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .stButton>button {
        background-color: #f39233 !important;
        color: white !important;
        border-radius: 8px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_all_html=True)

# 4. API BİLGİLERİ
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

def dukkan_ara(sorgu):
    # İstoç merkezli arama yapar
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}+istoç&key={API_KEY}&language=tr"
    response = requests.get(url).json()
    return response.get('results', [])

def detay_getir(place_id):
    # Dükkanın telefon numarasını almak için detay sorgusu
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number&key={API_KEY}&language=tr"
    response = requests.get(url).json()
    return response.get('result', {}).get('formatted_phone_number', 'Telefon Bulunamadı')

# 5. ARAYÜZ
st.title("Aradığın Ürün En Ucuz Burada!")
arama_kelimesi = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Dübel, Bant, Matkap...")

if st.button("Hemen Bul"):
    if arama_kelimesi:
        with st.spinner('Dükkanlar listeleniyor...'):
            sonuclar = dukkan_ara(arama_kelimesi)
            
            if sonuclar:
                st.success(f"'{arama_kelimesi}' için {len(sonuclar)} dükkan bulundu.")
                for dukkan in sonuclar:
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    puan = dukkan.get('rating', 'Yok')
                    place_id = dukkan.get('place_id')
                    
                    # Kart yapısı
                    with st.container():
                        st.markdown(f"""
                        <div class="result-card">
                            <h3>🏢 {isim}</h3>
                            <p>📍 <b>Adres:</b> {adres}</p>
                            <p>⭐ <b>Puan:</b> {puan}</p>
                        </div>
                        """, unsafe_allow_all_html=True)
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            # Harita Butonu
                            harita_url = f"https://www.google.com/maps/search/?api=1&query={isim}&query_place_id={place_id}"
                            st.markdown(f'<a href="{harita_url}" target="_blank"><button style="width:100%; cursor:pointer; padding:10px; background-color:#38b2ac; color:white; border:none; border-radius:5px;">📍 Haritada Gör</button></a>', unsafe_allow_all_html=True)
                        
                        with c2:
                            # WhatsApp butonu (Detaylardan telefon çekmeye çalışır)
                            telefon = detay_getir(place_id)
                            wa_link = f"https://wa.me/{telefon.replace(' ', '').replace('+', '')}?text={arama_kelimesi}%20fiyatini%20ogrenmek%20istiyorum"
                            st.markdown(f'<a href="{wa_link}" target="_blank"><button style="width:100%; cursor:pointer; padding:10px; background-color:#25D366; color:white; border:none; border-radius:5px;">💬 Fiyat Sor (WhatsApp)</button></a>', unsafe_allow_all_html=True)
                        st.write("---")
            else:
                st.error("Dükkan bulunamadı.")
    else:
        st.warning("Lütfen bir ürün ismi yazın.")
