import streamlit as st
import requests
import time

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARI
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    try:
        st.image("logo.png", width=220)
    except:
        st.title("🛒 En Ucuzu Burada")

# 4. FONKSİYONLAR
def dukkan_ara_gelismis(urun, lokasyon):
    sorgu = f"{urun} {lokasyon}"
    results = []
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}&key={API_KEY}&language=tr"
    try:
        response = requests.get(url).json()
        results.extend(response.get('results', []))
        
        # Sonraki sayfa varsa (maksimum 40 sonuç için 1 ek sayfa çekelim)
        next_token = response.get('next_page_token')
        if next_token:
            time.sleep(2) # Google zorunlu bekleme süresi
            url_next = f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={next_token}&key={API_KEY}&language=tr"
            response_next = requests.get(url_next).json()
            results.extend(response_next.get('results', []))
    except:
        pass
    return results

def detay_getir(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number,opening_hours,international_phone_number,photos&key={API_KEY}&language=tr"
    try:
        res = requests.get(url).json()
        return res.get('result', {})
    except:
        return {}

# 5. KATEGORİLER
st.write("---")
st.markdown("### 🏬 Alışveriş Kategorileri")
kat_gruplari = {
    "📱 Elektronik": ["Cep Telefonu", "Bilgisayar", "Televizyon"],
    "🛠️ Yapı & Sanayi": ["Hırdavat", "Elektrik", "Ambalaj"],
    "🏠 Ev & Yaşam": ["Mobilya", "Beyaz Eşya", "Züccaciye"]
}

secilen_kategori = ""
for grup, liste in kat_gruplari.items():
    with st.expander(grup):
        cols = st.columns(len(liste))
        for i, kat in enumerate(liste):
            # Her butona benzersiz bir key atıyoruz (Hata önleyici)
            if cols[i].button(kat, key=f"kat_btn_{kat}", use_container_width=True):
                secilen_kategori = kat

# 6. ARAMA ALANI
st.write("")
c1, c2 = st.columns([2, 1])
with c1:
    arama_input = st.text_input("Ne arıyorsunuz?", value=secilen_kategori, placeholder="Ürün veya marka...")
with c2:
    yer = st.text_input("Şehir / İlçe", value="İstoç")

sadece_acik = st.toggle("Sadece şu an açık olanları göster")

# 7. ARAMA MANTIĞI
if st.button("Dükkanları Listele", key="ana_arama_btn", use_container_width=True) or secilen_kategori:
    final_arama = arama_input if arama_input else secilen_kategori
    
    if final_arama and yer:
        with st.spinner('Sonuçlar yükleniyor...'):
            sonuclar = dukkan_ara_gelismis(final_arama, yer)
            
            if sonuclar:
                # Puan sıralaması
                sonuclar = sorted(sonuclar, key=lambda x: x.get('rating', 0), reverse=True)
                
                bulunan_sayisi = 0
                for index, dukkan in enumerate(sonuclar):
                    pid = dukkan.get('place_id')
                    detay = detay_getir(pid)
                    saatler = detay.get('opening_hours', {})
                    su_an_acik = saatler.get('open_now', False) if saatler else False
                    
                    if sadece_acik and not su_an_acik:
                        continue 
                    
                    bulunan_sayisi += 1
                    isim = dukkan.get('name')
                    tel = detay.get('formatted_phone_number') or detay.get('international_phone_number')
                    fotolar = detay.get('photos', [])
                    
                    with st.container():
                        st.divider()
                        col_img, col_txt = st.columns([1, 3])
                        
                        with col_img:
                            if fotolar:
                                foto_ref = fotolar[0].get('photo_reference')
                                foto_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={foto_ref}&key={API_KEY}"
                                st.image(foto_url, use_container_width=True)
                            else:
                                st.write("🖼️ Görsel Yok")

                        with col_txt:
                            st.subheader(isim)
                            st.write(f"📍 {dukkan.get('formatted_address')}")
                            if tel: st.write(f"📞 **Telefon:** {tel}")
                            st.write(f"⭐ Puan: {dukkan.get('rating', 'Yeni')} | {'✅ AÇIK' if su_an_acik else '❌ KAPALI'}")
                        
                        b1, b2 = st.columns(2)
                        with b1:
                            h_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}&query_place_id={pid}"
                            st.link_button("📍 Konum", h_link, key=f"map_{index}", use_container_width=True)
                        with b2:
                            if tel:
                                temiz_tel = "".join(filter(str.isdigit, tel))
                                if temiz_tel.startswith("0"): temiz_tel = "9" + temiz_tel
                                elif not temiz_tel.startswith("90"): temiz_tel = "90" + temiz_tel
                                wa_link = f"https://wa.me/{temiz_tel}?text=Merhaba, {final_arama} fiyatı alabilir miyim?"
                                st.link_button("💬 WhatsApp", wa_link, key=f"wa_{index}", type="primary", use_container_width=True)
                            else:
                                # Hata veren kısım: Key ekleyerek düzelttik
                                st.button("💬 No Yok", key=f"no_tel_{index}", disabled=True, use_container_width=True)
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen tüm alanları doldurun.")

st.caption("© 2025 enucuzuburada.com.tr")
