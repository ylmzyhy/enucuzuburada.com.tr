import streamlit as st

# 1. SAYFA AYARLARI (Hata almamak için en üstte olmalı)
st.set_page_config(
    page_title="En Ucuzu Burada",
    page_icon="🛒",
    layout="wide"
)

# 2. LOGO GÖSTERİMİ
# Logo zaten yüklü olduğu için artık düzgün görünecek
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", use_container_width=True)

# 3. TASARIM (CSS) - Hataları önlemek için sadeleştirildi
st.markdown("""
<style>
    h1 { color: #38b2ac; text-align: center; }
    .stButton>button {
        background-color: #f39233 !important;
        color: white !important;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
        height: 3em;
    }
    .result-card {
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 10px;
        background-color: #f9f9f9;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_all_html=True)

st.title("Aradığın Ürün En Ucuz Burada!")

# 4. ARAMA MOTORU
query = st.text_input("", placeholder="Ürün adı yazın (Örn: Bant, Matkap, Boya...)")

if st.button("Ucuzunu Bul"):
    if query:
        st.success(f"🔍 '{query}' için örnek dükkanlar:")
        
        # API anahtarın aktifleşene kadar siten bu dükkanları gösterecek
        veriler = [
            {"isim": "İstoç Ambalaj Market", "adres": "İstoç 24. Ada, Mahmutbey", "tel": "02121112233"},
            {"isim": "Yapı Malzeme Dünyası", "adres": "İstoç 12. Ada, Mahmutbey", "tel": "05320000000"}
        ]
        
        for dukkan in veriler:
            st.markdown(f"""
            <div class="result-card">
                <h3>🏢 {dukkan['isim']}</h3>
                <p>📍 {dukkan['adres']}</p>
                <p>📞 {dukkan['tel']}</p>
            </div>
            """, unsafe_allow_all_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"[📍 Haritada Gör](https://www.google.com/maps/search/{dukkan['isim'].replace(' ', '+')})")
            with c2:
                wa_msg = f"{query} fiyatını öğrenebilir miyim?"
                st.markdown(f"[💬 WhatsApp'tan Fiyat Sor](https://wa.me/{dukkan['tel']}?text={wa_msg})")
            st.divider()
    else:
        st.warning("Lütfen bir ürün ismi girin.")

st.markdown("---")
st.write("© 2025 enucuzuburada.com.tr")
