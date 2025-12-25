import streamlit as st

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. LOGO GÖSTERİMİ
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", width=300)

# 3. TASARIM (CSS)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #f39233 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    h1 { color: #38b2ac !important; text-align: center; }
    .shop-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 10px;
        background-color: #fcfcfc;
    }
    </style>
    """, unsafe_allow_all_html=True)

st.title("Aradığın Ürün En Ucuz Burada!")

# 4. ARAMA KISMI
search_query = st.text_input("", placeholder="Ürün adını yazın... (Örn: Bant)")

if st.button("Ucuzunu Bul"):
    if search_query:
        st.success(f"🔍 '{search_query}' için örnek sonuçlar listeleniyor:")
        
        # ÖRNEK VERİLER (API Key alınca burası gerçek verilerle dolacak)
        ornek_dukkanlar = [
            {"ad": "İstoç Ambalaj Dünyası", "adres": "İstoç 24. Ada No: 45, Mahmutbey", "tel": "0212 111 22 33"},
            {"ad": "Ucuz Bant Pazarı", "adres": "İstoç 12. Ada No: 12, Mahmutbey", "tel": "0212 444 55 66"}
        ]

        for dukkan in ornek_dukkanlar:
            st.markdown(f"""
            <div class="shop-card">
                <h4>🏢 {dukkan['ad']}</h4>
                <p>📍 {dukkan['adres']}</p>
                <p>📞 {dukkan['tel']}</p>
            </div>
            """, unsafe_allow_all_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.button(f"📍 Haritada Gör ({dukkan['ad']})")
            with c2:
                st.success(f"💬 WhatsApp'tan Fiyat Sor")
    else:
        st.warning("Lütfen bir kelime yazın.")
