import streamlit as st
import pandas as pd
import requests

# 1. SAYFA AYARLARI (En üstte olmalı)
st.set_page_config(
    page_title="En Ucuzu Burada | Yerel Fiyat Arama",
    page_icon="🛒",
    layout="wide"
)

# 2. LOGO GÖSTERİMİ
try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=300)
except:
    st.warning("⚠️ logo.png bulunamadı. Lütfen GitHub'a bu isimle yükleyin.")

# 3. TASARIM (CSS) - Turuncu Buton ve Turkuaz Başlıklar
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stButton>button {
        background-color: #f39233 !important;
        color: white !important;
        border-radius: 10px !important;
        height: 3em !important;
        width: 100% !important;
        font-weight: bold !important;
        border: none !important;
    }
    h1 { color: #38b2ac !important; text-align: center; font-family: 'sans-serif'; }
    .shop-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 15px;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_all_html=True)

st.title("Aradığın Ürün En Ucuz Burada!")
st.markdown("<p style='text-align: center; color: gray;'>İstoç ve çevresindeki en uygun dükkanları anında bul.</p>", unsafe_allow_all_html=True)

# 4. ARAMA MOTORU FONKSİYONU
# NOT: Buraya daha önce kullandığın Google API Key'ini yazmalısın
API_KEY = "BURAYA_GOOGLE_API_ANAHTARINI_YAZ"

def get_places(query):
    # İstoç/Mahmutbey odaklı arama
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}+istoç&key={API_KEY}&language=tr"
    response = requests.get(url).json()
    return response.get('results', [])

# 5. ARAMA ARAYÜZÜ
search_query = st.text_input("", placeholder="Örn: Koli Bandı, Streç Film, Ambalaj...", help="Ürün adını yazın ve Ara'ya basın.")

if st.button("Ucuzunu Bul"):
    if search_query:
        results = get_places(search_query)
        
        if results:
            st.success(f"🔍 '{search_query}' için {len(results)} dükkan bulundu.")
            
            for place in results:
                name = place.get('name')
                # Plus code yerine gerçek açık adresi alıyoruz
                address = place.get('formatted_address', 'Adres bulunamadı')
                rating = place.get('rating', 'Yok')
                place_id = place.get('place_id')
                map_link = f"https://www.google.com/maps/search/?api=1&query={name}&query_place_id={place_id}"
                
                # Kart Tasarımı
                with st.container():
                    st.markdown(f"""
                    <div class="shop-card">
                        <h3>🏢 {name}</h3>
                        <p>📍 <b>Adres:</b> {address}</p>
                        <p>⭐ <b>Puan:</b> {rating}</p>
                    </div>
                    """, unsafe_allow_all_html=True)
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f'<a href="{map_link}" target="_blank"><button style="width:100%; background-color:#38b2ac; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">📍 Haritada Gör</button></a>', unsafe_allow_all_html=True)
                    with c2:
                        # WhatsApp Fiyat Sor Butonu
                        wa_msg = f"Merhaba, {search_query} fiyatını öğrenebilir miyim?"
                        wa_url = f"https://wa.me/?text={wa_msg}"
                        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">💬 Fiyat Sor (WhatsApp)</button></a>', unsafe_allow_all_html=True)
                    st.write("") # Boşluk
        else:
            st.error("Üzgünüz, aradığınız kriterde bir dükkan bulunamadı.")
    else:
        st.warning("Lütfen bir ürün adı girin.")

# 6. FOOTER
st.markdown("---")
st.markdown("<p style='text-align: center; color: silver;'>enucuzuburada.com.tr | 2025</p>", unsafe_allow_all_html=True)
