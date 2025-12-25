import streamlit as st
import pandas as pd
import requests

# 1. SAYFA AYARLARI (Mutlaka en üstte olmalı)
st.set_page_config(
    page_title="En Ucuzu Burada | Yerel Fiyat Arama",
    page_icon="🛒",
    layout="wide"
)

# 2. LOGO VE GÖRSEL AYARLAR
try:
    # Logonun ortalı ve şık durması için sütun kullanıyoruz
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=300)
except:
    st.warning("⚠️ logo.png dosyası GitHub'da bulunamadı. Lütfen yükleyin.")

# 3. TASARIM VE RENK AYARLARI (CSS)
st.markdown("""
    <style>
    /* Ana Başlık Rengi (Turkuaz) */
    h1 {
        color: #38b2ac !important;
        text-align: center;
    }
    /* Buton Tasarımı (Turuncu) */
    .stButton>button {
        background-color: #f39233 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        height: 3em !important;
        width: 100% !important;
        font-weight: bold !important;
    }
    /* Haritaya Git Butonu İçin Özel Stil */
    .map-button {
        background-color: #38b2ac;
        color: white;
        padding: 8px 15px;
        text-decoration: none;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
    }
    /* Bilgi Notu */
    .info-text {
        text-align: center;
        color: #666;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_all_html=True)

# 4. BAŞLIK VE ARAMA ÇUBUĞU
st.title("Aradığın Ürün En Ucuz Burada!")
st.markdown("<p class='info-text'>Çevrendeki dükkanları ve en uygun fiyatlı yerleri hemen bul.</p>", unsafe_allow_all_html=True)

# Arama motoru fonksiyonunuzu buraya entegre ediyoruz
search_query = st.text_input("", placeholder="Örn: Koli Bandı, Matkap, Boya...", help="Aramak istediğiniz ürünü yazın.")

# 5. ARAMA BUTONU VE SONUÇLAR
if st.button("Ucuzunu Bul"):
    if search_query:
        st.info(f"🔍 '{search_query}' için dükkanlar aranıyor...")
        
        # BURASI SİZİN GOOGLE MAPS VERİ ÇEKME KODUNUZUN GELECEĞİ YER
        # Örnek tablo yapısını gösteriyorum:
        
        data = {
            "Dükkan Adı": ["Örnek Yapı Market", "Ucuzcu Bantçı", "Hırdavat Dünyası"],
            "Adres": ["Mahmutbey Mah. 2450. Sok No:5", "İstoç 24. Ada No:10", "Bağcılar Cad. No:100"],
            "Telefon": ["0212 111 22 33", "0212 444 55 66", "0532 000 00 00"],
            "Konum": ["https://maps.google.com", "https://maps.google.com", "https://maps.google.com"]
        }
        
        df = pd.DataFrame(data)
        
        # Tabloyu şık bir şekilde gösterelim
        for index, row in df.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([2, 3, 1])
                c1.subheader(row["Dükkan Adı"])
                c2.write(f"📍 {row['Adres']}\n\n📞 {row['Telefon']}")
                # WhatsApp ve Harita Butonları
                whatsapp_url = f"https://wa.me/{row['Telefon'].replace(' ', '')}?text={search_query}%20fiyatını%20öğrenebilir%20miyim?"
                c3.markdown(f"[📍 Harita]({row['Konum']})", unsafe_allow_all_html=True)
                c3.markdown(f"[💬 Fiyat Sor]({whatsapp_url})", unsafe_allow_all_html=True)
                st.divider()
    else:
        st.warning("Lütfen bir ürün adı girin.")

# 6. ALT BİLGİ (Footer)
st.markdown("---")
st.markdown("<p style='text-align: center;'>© 2025 enucuzuburada.com.tr - Tüm Hakları Saklıdır.</p>", unsafe_allow_all_html=True)
