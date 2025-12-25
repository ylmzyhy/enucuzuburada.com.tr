import streamlit as st
import requests
import time

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
    "🛠️ Sanayi": ["Hırdavat", "Elektrik", "Ambalaj"],
    "🏠 Yaşam": ["Mobilya", "Dekorasyon", "Mutfak"]
}

secilen_kategori = ""
for grup, liste in kat_gruplari.items():
    with st.expander(grup):
        cols = st.columns(len(liste))
        for i, kat in enumerate(liste):
            # Buton Key'lerini sabitledik
            if cols[i].button(kat, key=f"btn_kat_{kat}", use_container_width=True):
                secilen_kategori = kat

# 6. ARAMA ALANI
st.write("")
c1, c2 = st.columns([2, 1])
with c1:
    arama_input = st.text_input("Ürün veya Marka Yazın", value=secilen_kategori, key="main_search_input")
with c2:
    yer = st.text_input("Konum (İlçe/Şehir)", value="İstanbul", key="main_loc_input")

# 7. ARAMA MANTIĞI
if st.button("Dükkanları Bul", key="submit_btn", use_container_width=True) or secilen_kategori:
    final_arama = arama_input if arama_input else secilen_kategori
    
    if final_arama and yer:
        with st.spinner('Dükkanlar getiriliyor...'):
            sonuclar = dukkan_ara(final_arama, yer)
            
            if sonuclar:
                # Puanı yüksek olanları başa al
                sonuclar = sorted(sonuclar, key=lambda x: x.get('rating', 0), reverse=True)
                
                for idx, dukkan in enumerate(sonuclar):
                    pid = dukkan.get('place_id', f"no_id_{idx}")
                    detay = detay_getir(pid)
                    
                    isim = dukkan.get('name', 'İşletme Adı Yok')
                    adres = dukkan.get('formatted_address', 'Adres Bilgisi Yok')
                    tel = detay.get('formatted_phone_number') or detay.get('international_phone_number')
                    fotolar = detay.get('photos', [])
                    
                    # Açık/Kapalı Durumu
                    saatler = detay.get('opening_hours', {})
                    durum = "✅ AÇIK" if saatler.get('open_now') else "❌ KAPALI"
                    
                    with st.container():
                        st.divider()
                        col_img, col_txt = st.columns([1, 3])
                        
                        with col_img:
                            if fotolar:
                                f_ref = fotolar[0].get('photo_reference')
                                f_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={f_ref}&key={API_KEY}"
                                st.image(f_url, use_container_width=True)
                            else:
                                st.write("🖼️ Fotoğraf Mevcut Değil")

                        with col_txt:
                            st.subheader(isim)
                            st.write(f"📍 {adres}")
                            if tel: st.write(f"📞 **Telefon:** {tel}")
                            st.write(f"⭐ Puan: {dukkan.get('rating', 'Yeni')} | {durum}")
                        
                        # BUTONLAR - ID Çakışmasını önlemek için IDX kullanıyoruz
                        b1, b2 = st.columns(2)
                        with b1:
                            m_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}&query_place_id={pid}"
                            st.link_button("📍 Haritada Göster", m_link, key=f"loc_link_{idx}", use_container_width=True)
                        with b2:
                            if tel:
                                clean_tel = "".join(filter(str.isdigit, tel))
                                if clean_tel.startswith("0"): clean_tel = "9" + clean_tel
                                elif not clean_tel.startswith("90"): clean_tel = "90" + clean_tel
                                
                                wa_link = f"https://wa.me/{clean_tel}?text=Merhaba, {final_arama} fiyatı öğrenebilir miyim?"
                                st.link_button("💬 WhatsApp İletişim", wa_link, key=f"wa_link_{idx}", type="primary", use_container_width=True)
                            else:
                                st.button("📞 No Bulunamadı", key=f"no_tel_{idx}", disabled=True, use_container_width=True)
            else:
                st.warning("Aradığınız dükkan bulunamadı.")
    else:
        st.info("Lütfen bir ürün ismi ve konum yazarak aramayı başlatın.")

st.caption("© 2025 enucuzuburada.com.tr")
