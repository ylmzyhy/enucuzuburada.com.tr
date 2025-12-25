import streamlit as st

# 1. AYARLAR
st.set_page_config(page_title="En Ucuzu Burada", layout="wide")

# 2. LOGO
try:
    st.image("logo.png", width=250)
except:
    st.write("Logo Yükleniyor...")

# 3. BAŞLIK VE ARAMA (Hata riskini sıfıra indirmek için sadeleştirildi)
st.title("En Ucuzu Burada")
st.subheader("Aradığın ürün için dükkanları bul")

# Arama kutusu
arama = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Bant, Matkap...")

if st.button("Ara"):
    if arama:
        st.success(f"'{arama}' için dükkanlar aranıyor...")
        
        # Örnek dükkan listesi
        col1, col2 = st.columns(2)
        with col1:
            st.info("🏢 İstoç Ambalaj")
            st.write("📍 İstoç 24. Ada")
            st.write("📞 0212 111 22 33")
        with col2:
            st.info("🏢 Hırdavat Dünyası")
            st.write("📍 İstoç 12. Ada")
            st.write("📞 0532 000 00 00")
    else:
        st.warning("Lütfen bir kelime yazın.")

# 4. ALT BİLGİ
st.markdown("---")
st.write("enucuzuburada.com.tr")
