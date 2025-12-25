import streamlit as st
import requests
import time

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARI
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO
c_l1, c_l2, c_l3 = st.columns([1, 1, 1])
with c_l2:
    try:
        st.image("logo.png", width=220)
    except:
        st.title("🛒 En Ucuzu Burada")

# 4. FONKSİYONLAR
def dukkan_ara_bolca(urun, lokasyon):
    sorgu = f"{urun} {lokasyon}"
    hepsi = []
    # 1. Sayfa
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}&key={API_KEY}&language=tr"
    try:
        r = requests.get(url).json()
        hepsi.extend(r.get('results', []))
        # Google'ın sonraki sayfa sistemi bazen geç yüklenir, o yüzden 2. sayfayı dikkatli çekiyoruz
        token = r.get('next_page_token')
        if token:
            time.sleep(2) # Google zorunlu bekletir
            url2 = f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={token}&key={API_KEY}&language=tr"
            r2 = requests.get(url2).json()
            hepsi.extend(r2.get('results', []))
    except:
        pass
    return hepsi

def detay_getir(place_id):
    if not place_id: return {}
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number,opening_hours,international_phone_number,photos&key={API_KEY}&language=tr"
    try:
        return requests.get(url).json().get('result', {})
    except:
        return {}

# 5. KATEGORİLER
st.write("---")
st.markdown("### 🏬 Popüler Kategoriler")
kats = {
    "📱 Elektronik": ["Cep Telefonu", "Bilgisayar", "Beyaz Eşya"],
    "🛠️ Yapı & Sanayi": ["Hırdavat", "Elektrik", "Ambalaj"],
    "🏠 Ev & Yaşam": ["Mobilya", "Dekorasyon", "Mutfak"]
}

secilen = ""
for g_ad, liste in kats.items():
    with st.expander(g_ad):
        cols = st.columns(len(liste))
        for i, k_ad in enumerate(liste):
            if cols[i].button(k_ad, key=f"k_b_{k_ad}", use_container_width=True):
                secilen = k_ad

# 6. ARAMA ALANI
st.write("")
col_a, col_b = st.columns([2, 1])
with col_a:
    input_ara = st.text_input("Ürün veya Marka", value=secilen, key="input_q")
with col_b:
    input_yer = st.text_input("Konum (İlçe/Şehir)", value="İstanbul", key="input_l")

# 7. ARAMA MANTIĞI
if st.button("Dükkanları Bul", key="main_go", use_container_width=True) or secilen:
    sorgu_terimi = input_ara if input_ara else secilen
    
    if sorgu_terimi and input_yer:
        with st.spinner('Dükkanlar listeleniyor...'):
            veriler = dukkan_ara_bolca(sorgu_terimi, input_yer)
            
            if veriler:
                # Puan sıralaması
                veriler = sorted(veriler, key=lambda x: x.get('rating', 0), reverse=True)
                
                for i, d in enumerate(veriler):
                    p_id = d.get('place_id', f"idx_{i}")
                    bilgi = detay_getir(p_id)
                    
                    isim = d.get('name', 'İsimsiz İşletme')
                    adr = d.get('formatted_address', 'Adres yok')
                    tel = bilgi.get('formatted_phone_number') or bilgi.get('international_phone_number')
                    puan = d.get('rating', 'Yeni')
                    
                    # Açık mı?
                    saat = bilgi.get('opening_hours', {})
                    durum = "✅ AÇIK" if saat.get('open_now') else "❌ KAPALI"
                    
                    with st.container():
                        st.divider()
                        c_img, c_txt = st.columns([1, 3])
                        
                        with c_img:
                            fotos = bilgi.get('photos', [])
                            if fotos:
                                f_ref = fotos[0].get('photo_reference')
                                f_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={f_ref}&key={API_KEY}"
                                st.image(f_url, use_container_width=True)
                            else:
                                st.write("🖼️ Fotoğraf Yok")

                        with c_txt:
                            st.subheader(isim)
                            st.write(f"📍 {adr}")
                            if tel: st.write(f"📞 **Telefon:** {tel}")
                            st.write(f"⭐ Puan: {puan} | {durum}")
                        
                        # BUTONLAR - En güvenli key ataması
                        bt1, bt2 = st.columns(2)
                        with bt1:
                            m_url = f"https://www.google.com/maps/search/?api=1&query={isim}&query_place_id={p_id}"
                            st.link_button("📍 Haritada Göster", m_url, key=f"map_{i}_{p_id}", use_container_width=True)
                        with bt2:
                            if tel:
                                t_temiz = "".join(filter(str.isdigit, tel))
                                if t_temiz.startswith("0"): t_temiz = "9" + t_temiz
                                elif not t_temiz.startswith("90"): t_temiz = "90" + t_temiz
                                w_url = f"https://wa.me/{t_temiz}?text=Merhaba, {sorgu_terimi} fiyatı alabilir miyim?"
                                st.link_button("💬 WhatsApp", w_url, key=f"wa_{i}_{p_id}", type="primary", use_container_width=True)
                            else:
                                st.button("📞 No Yok", key=f"none_{i}_{p_id}", disabled=True, use_container_width=True)
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.info("Lütfen bir ürün ve konum girin.")

st.caption("© 2025 enucuzuburada.com.tr")
