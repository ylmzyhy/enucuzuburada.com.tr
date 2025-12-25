import streamlit as st

# 1. SAYFA AYARLARI (Hata almamak için mutlaka en üstte olmalı)
st.set_page_config(
    page_title="En Ucuzu Burada",
    page_icon="🛒",
    layout="wide"
)

# 2. LOGO GÖSTERİMİ
try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Dosya adınız tam olarak logo.png olmalı
        st.image("logo.png", width=300)
except Exception:
    st.info("Logo dosyası yükleniyor...")

# 3. TASARIM VE RENKLER (CSS)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    h1 { color: #38b2ac !important; text-align: center; }
    .stButton>button {
        background-color: #f39233 !important;
        color: white !important;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
        border: none;
        height: 3em;
    }
    .result-card {
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_all_html=True)

st.title("Aradığın Ürün En Ucuz Burada!")

# 4. ARAMA MOTORU
query = st.text_input("", placeholder="Ürün adı yazın (Örn: Bant, Matkap, Boya...)")

if st.button("Ucuzunu Bul"):
    if query:
        st.success(f"🔍 '{query}' için dükkanlar listeleniyor...")
        
        # API AKTİF OLANA KADAR ÖRNEK VERİLER (Sitenin boş kalmaması için)
        veriler = [
            {"isim": "İstoç Ambalaj Market", "adres": "İstoç 24. Ada No: 45, Mahmutbey", "tel": "02121112233"},
            {"isim": "Yapı Malzeme Dünyası", "adres": "İstoç 12. Ada No: 10, Mahmutbey", "tel": "05320000000"}
        ]
        
        for dukkan in veriler:
            with st.container():
                st.markdown(f"""
                <div class="result-card">
                    <h3>🏢 {dukkan['isim']}</h3>
                    <p>📍 <b>Adres:</b> {dukkan['adres']}</p>
                </div>
                """, unsafe_allow_all_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    # Harita linki
                    st.markdown(f"[📍 Haritada Gör](https://www.google.com/maps/search/{dukkan['isim'].replace(' ', '+')})")
                with c2:
                    # WhatsApp Fiyat Sor butonu
                    wa_msg = f"{query} fiyatını öğrenebilir miyim?"
                    st.markdown(f"[💬 WhatsApp'tan Fiyat Sor](https://wa.me/{dukkan['tel']}?text={wa_msg})")
                st.divider()
    else:
        st.warning("Lütfen bir ürün ismi girin.")

st.markdown("---")
st.write("© 2025 enucuzuburada.com.tr")
