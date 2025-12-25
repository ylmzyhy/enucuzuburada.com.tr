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

# 4. FONKSİYONLAR (Hata Önleyicili)
def dukkan_ara_gelismis(urun, lokasyon):
    sorgu = f"{urun} {lokasyon}"
    all_results = []
    
    # 1. Sayfa Çekimi
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}&key={API_KEY}&language=tr"
    try:
        res = requests.get(url).json()
        all_results.extend(res.get('results', []))
        
        # Daha fazla sonuç için token varsa 2. sayfayı çek
        next_token = res.get('next_page_token')
        if next_token:
            time.sleep(2) # Google zorunlu bekleme süresi
            url_next = f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={next_token}&key={API_KEY}&language=tr"
            res_next = requests.get(url_next).json()
            all_results.extend(res_next.get('results', []))
    except Exception as e:
        st.error(f"Arama hatası: {e}")
    return all_results

def detay_getir(pid):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={pid}&fields=formatted_phone_number,opening_hours,international_phone_number,photos&key={API_KEY}&language=tr"
    try:
        r = requests.get(url).json()
        return r.get('result', {})
    except:
        return {}

# 5. KATEGORİLER (Sadeleştirilmiş ve Güvenli)
st.write("---")
st.markdown("### 🏬 Alışveriş Kategorileri")
kat_gruplari = {
    "📱 Elektronik": ["Cep Telefonu", "Bilgisayar", "Beyaz Eşya"],
    "🛠️ Yapı & Sanayi": ["Hırdavat", "Elektrik", "Ambalaj"],
    "🏠 Ev & Yaşam": ["Mobilya", "Dekorasyon", "Mutfak"]
}

secilen_kategori = ""
for grup, liste in kat_gruplari.items():
    with st.expander(grup):
        cols = st.columns(len(liste))
        for i, kat in enumerate(liste):
            # Benzersiz KEY ekleyerek çakışmayı %100 önledik
            if cols[i].button(kat, key=f"k_btn_{kat}", use_container_width=True):
                secilen_kategori = kat

# 6. ARAMA ALANI
st.write("")
c1, c2 = st.columns([2, 1])
with c1:
    arama_input = st.text_input("Ne arıyorsunuz?", value=secilen_kategori, placeholder="Ürün veya marka...", key="input_text")
with c2:
    yer = st.text_input("Şehir / İlçe", value="İstoç", key="input_loc")

sadece_acik = st.toggle("Sadece şu an açık olanları göster", key="toggle_open")

# 7. ARAMA MANTIĞI
if st.button("Dükkanları Listele", key="main_search_btn", use_container_width=True) or (secilen_kategori != ""):
    final_arama = arama_input if arama_input else secilen_kategori
    
    if final_arama and yer:
        with st.spinner('Tüm sonuçlar taranıyor, lütfen bekleyin...'):
            sonuclar = dukkan_ara_gelismis(final_arama, yer)
            
            if sonuclar:
                # Puanı yüksek olanları başa al
                sonuclar = sorted(sonuclar, key=lambda x: x.get('rating', 0), reverse=True)
                
                bulunan_sayisi = 0
                for index, dukkan in enumerate(sonuclar):
                    pid = dukkan.get('place_id', f"no_id_{index}")
                    detay = detay_getir(pid)
                    
                    saatler = detay.get('opening_hours', {})
                    su_an_acik = saatler.get('open_now', False) if saatler else False
                    
                    if sadece_acik and not su_an_acik:
                        continue 
                    
                    bulunan_sayisi += 1
                    isim = dukkan.get('name', 'Bilinmeyen İşletme')
                    tel = detay.get('formatted_phone_number') or detay.get('international_phone_number')
                    fotolar = detay.get('photos', [])
                    
                    with st.container():
                        st.divider()
                        col_img, col_txt = st.columns([1, 3])
                        with col_img:
                            if fotolar:
                                f_ref = fotolar[0].get('photo_reference')
                                f_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={f_ref}&key={API_KEY}"
                                st.image(f_url, use_container_width=True)
                            else:
                                st.write("🖼️ Görsel Yok")
                        with col_txt:
                            st.subheader(isim)
                            st.write(f"📍 {dukkan.get('formatted_address', 'Adres bulunamadı')}")
                            if tel: st.write(f"📞 **Telefon:** {tel}")
                            st.write(f"⭐ Puan: {dukkan.get('rating', 'Yeni')} | {'✅ AÇIK' if su_an_acik else '❌ KAPALI'}")
                        
                        # BUTONLAR - BURASI KRİTİK! Benzersiz KEY tanımlıyoruz.
                        b1, b2 = st.columns(2)
                        with b1:
                            m_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}&query_place_id={pid}"
                            st.link_button("📍 Konum", m_link, key=f"map_btn_{pid}_{index}", use_container_width=True)
                        with b2:
                            if tel:
                                temiz_tel = "".join(filter(str.isdigit, tel))
                                if temiz_tel.startswith("0"): temiz_tel = "9" + temiz_tel
                                elif not temiz_tel.startswith("90"): temiz_tel = "90" + temiz_tel
                                wa_link = f"https://wa.me/{temiz_tel}?text=Merhaba, {final_arama} fiyatı alabilir miyim?"
                                st.link_button("💬 WhatsApp", wa_link, key=f"wa_btn_{pid}_{index}", type="primary", use_container_width=True)
                            else:
                                st.button("💬 No Bulunamadı", key=f"no_tel_btn_{pid}_{index}", disabled=True, use_container_width=True)
                
                st.success(f"Toplam {bulunan_sayisi} dükkan listelendi.")
            else:
                st.warning("Bu kriterlere uygun yer bulunamadı.")
    else:
        st.error("Ürün ve konum alanlarını doldurun.")

st.caption("© 2025 enucuzuburada.com.tr")
