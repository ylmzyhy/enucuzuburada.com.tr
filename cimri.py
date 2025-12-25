import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARI
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO
col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
with col_l2:
    try:
        st.image("logo.png", width=220)
    except:
        st.title("🛒 En Ucuzu Burada")

# 4. FONKSİYONLAR
def dukkan_ara(urun, lokasyon):
    sorgu = f"{urun} {lokasyon}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}&key={API_KEY}&language=tr"
    try:
        res = requests.get(url).json()
        return res.get('results', [])
    except:
        return []

def detay_getir(pid):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={pid}&fields=formatted_phone_number,opening_hours,international_phone_number,photos&key={API_KEY}&language=tr"
    try:
        r = requests.get(url).json()
        return r.get('result', {})
    except:
        return {}

# 5. KATEGORİLER
st.write("---")
st.markdown("### 🏬 Popüler Kategoriler")
kat_gruplari = {
    "📱 Elektronik": ["Cep Telefonu", "Bilgisayar", "Beyaz Eşya"],
    "🛠️ Yapı & Sanayi": ["Hırdavat", "Elektrik", "Ambalaj"],
    "🏠 Ev & Yaşam": ["Mobilya", "Dekorasyon", "Mutfak"]
}

secilen_kat = ""
for grup, liste in kat_gruplari.items():
    with st.expander(grup):
        cols = st.columns(len(liste))
        for i, kat in enumerate(liste):
            if cols[i].button(kat, key=f"k_btn_{kat}"):
                secilen_kat = kat

# 6. ARAMA ALANI
st.write("")
c1, c2 = st.columns([2, 1])
with c1:
    arama_input = st.text_input("Ürün veya Marka", value=secilen_kat, key="search_input")
with c2:
    yer = st.text_input("Şehir / İlçe", value="İstanbul", key="loc_input")

# 7. ARAMA MANTIĞI
if st.button("Dükkanları Listele", key="submit_button", use_container_width=True) or secilen_kat:
    final_ara = arama_input if arama_input else secilen_kat
    
    if final_ara and yer:
        with st.spinner('Sonuçlar yükleniyor...'):
            sonuclar = dukkan_ara(final_ara, yer)
            
            if sonuclar:
                # Puan sıralaması (Yüksek puanlılar üstte)
                sonuclar = sorted(sonuclar, key=lambda x: x.get('rating', 0), reverse=True)
                
                for idx, dukkan in enumerate(sonuclar):
                    pid = dukkan.get('place_id')
                    detay = detay_getir(pid)
                    
                    isim = dukkan.get('name', 'İsimsiz Dükkan')
                    tel = detay.get('formatted_phone_number') or detay.get('international_phone_number')
                    saatler = detay.get('opening_hours', {})
                    durum = "✅ AÇIK" if saatler.get('open_now') else "❌ KAPALI"
                    
                    with st.container():
                        st.divider()
                        col_img, col_txt = st.columns([1, 3])
                        
                        with col_img:
                            fotos = detay.get('photos', [])
                            if fotos:
                                f_ref = fotos[0].get('photo_reference')
                                f_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={f_ref}&key={API_KEY}"
                                st.image(f_url, use_container_width=True)
                            else:
                                st.write("🖼️ Fotoğraf Yok")

                        with col_txt:
                            st.subheader(isim)
                            st.write(f"📍 {dukkan.get('formatted_address')}")
                            if tel: st.write(f"📞 **Telefon:** {tel}")
                            st.write(f"⭐ Puan: {dukkan.get('rating', 'Yeni')} | {durum}")
                        
                        # BUTONLAR (Hata önleyici benzersiz anahtarlar eklendi)
                        b1, b2 = st.columns(2)
                        with b1:
                            m_link = f"https://www.google.com/maps/search/?api=1&query={isim}&query_place_id={pid}"
                            st.link_button("📍 Haritada Göster", m_link, key=f"loc_{idx}_{pid}", use_container_width=True)
                        with b2:
                            if tel:
                                clean_tel = "".join(filter(str.isdigit, tel))
                                if clean_tel.startswith("0"): clean_tel = "9" + clean_tel
                                elif not clean_tel.startswith("90"): clean_tel = "90" + clean_tel
                                wa_link = f"https://wa.me/{clean_tel}?text=Merhaba, {final_ara} fiyatı alabilir miyim?"
                                st.link_button("💬 WhatsApp", wa_link, key=f"wa_{idx}_{pid}", type="primary", use_container_width=True)
                            else:
                                st.button("📞 No Bulunamadı", key=f"none_{idx}_{pid}", disabled=True, use_container_width=True)
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.info("Lütfen arama yapın.")

st.caption("© 2025 enucuzuburada.com.tr")
