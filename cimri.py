import streamlit as st
import requests

# 1. TEMEL SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", layout="wide")

# 2. GOOGLE API ANAHTARIN (Resimden aldım)
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO (Varsa gösterir, yoksa isim yazar)
try:
    st.image("logo.png", width=250)
except:
    st.title("🛒 En Ucuzu Burada")

# 4. GOOGLE MAPS ARAMA FONKSİYONU
def dukkan_getir(sorgu):
    # İstoç bölgesindeki dükkanları filtreleyerek arar
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}+istoç&key={API_KEY}&language=tr"
    response = requests.get(url).json()
    return response.get('results', [])

# 5. ARAYÜZ TASARIMI
st.write("---")
arama_terimi = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Dübel, Bant, Koli...")

if st.button("Dükkanları Bul"):
    if arama_terimi:
        with st.spinner('İstoç dükkanları taranıyor...'):
            sonuclar = dukkan_getir(arama_terimi)
            
            if sonuclar:
                st.success(f"'{arama_terimi}' için {len(sonuclar)} dükkan listeleniyor:")
                
                for dukkan in sonuclar:
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    puan = dukkan.get('rating', 'Puan Yok')
                    
                    # Dükkan Bilgileri
                    st.subheader(f"🏢 {isim}")
                    st.write(f"📍 **Adres:** {adres}")
                    st.write(f"⭐ **Puan:** {puan}")
                    
                    # Linkler
                    c1, c2 = st.columns(2)
                    with c1:
                        harita_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}"
                        st.markdown(f"[📍 Haritada Gör]({harita_link})")
                    with c2:
                        wa_mesaj = f"Merhaba, {arama_terimi} fiyatını öğrenebilir miyim?"
                        wa_link = f"https://wa.me/?text={wa_mesaj}"
                        st.markdown(f"[💬 WhatsApp'tan Sor]({wa_link})")
                    st.write("---")
            else:
                st.warning("Aradığınız kriterlere uygun bir dükkan bulunamadı.")
    else:
        st.error("Lütfen bir ürün adı yazın.")

# 6. ALT BİLGİ
st.caption("© 2025 enucuzuburada.com.tr")
