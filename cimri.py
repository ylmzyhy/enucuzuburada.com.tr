import streamlit as st
import requests

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
def dukkan_ara(urun, lokasyon):
    sorgu = f"{urun} {lokasyon}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}&key={API_KEY}&language=tr"
    response = requests.get(url).json()
    return response.get('results', [])

def detay_getir(place_id):
    fields = "formatted_phone_number,opening_hours,international_phone_number,photos"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={API_KEY}&language=tr"
    res = requests.get(url).json()
    return res.get('result', {})

# 5. ARAYÜZ VE KATEGORİLER
st.write("---")

# Hızlı Kategoriler
st.markdown("### ⚡ Hızlı Kategoriler")
kategoriler = ["Hırdavat", "Elektrik", "Ambalaj", "İş Güvenliği", "Civata & Somun", "Rulman"]
cols = st.columns(len(kategoriler))

secilen_kategori = ""
for i, kat in enumerate(kategoriler):
    if cols[i].button(kat, use_container_width=True):
        secilen_kategori = kat

st.write("") # Boşluk

# Arama Çubukları
c1, c2 = st.columns([2, 1])
with c1:
    arama_input = st.text_input("Ne arıyorsunuz?", value=secilen_kategori, placeholder="Örn: Matkap, Kaynak Makinesi...")
with c2:
    yer = st.text_input("Nerede?", value="İstoç", placeholder="İlçe veya Sanayi Sitesi...")

# Filtreleme Seçeneği
sadece_acik = st.toggle("Sadece şu an açık olan dükkanları göster")

# 6. ARAMA MANTIĞI
if st.button("Dükkanları ve Fiyat Sorulacak Yerleri Bul", use_container_width=True) or secilen_kategori:
    arama_terimi = arama_input if arama_input else secilen_kategori
    
    if arama_terimi and yer:
        with st.spinner(f'{yer} bölgesinde en iyi yerler aranıyor...'):
            sonuclar = dukkan_ara(arama_terimi, yer)
            
            if sonuclar:
                bulunan_sayisi = 0
                for dukkan in sonuclar:
                    pid = dukkan.get('place_id')
                    detay = detay_getir(pid)
                    saatler = detay.get('opening_hours', {})
                    
                    # Açık Filtresi Kontrolü
                    su_an_acik = saatler.get('open_now', False) if saatler else False
                    if sadece_acik and not su_an_acik:
                        continue # Kapalıysa bu dükkanı atla
                    
                    bulunan_sayisi += 1
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    puan = dukkan.get('rating', 'Yeni')
                    tel = detay.get('formatted_phone_number') or detay.get('international_phone_number')
                    fotolar = detay.get('photos', [])
                    
                    acik_mi_text = "✅ ŞİMDİ AÇIK" if su_an_acik else "❌ ŞİMDİ KAPALI"
                    calisma_saati = "Belirtilmemiş"
                    if saatler:
                        gunluk_liste = saatler.get('weekday_text', [])
                        if gunluk_liste:
                            calisma_saati = gunluk_liste[0].split(": ", 1)[-1]

                    with st.container():
                        st.divider()
                        col_img, col_txt = st.columns([1, 3])
                        
                        with col_img:
                            if fotolar:
                                foto_ref = fotolar[0].get('photo_reference')
                                foto_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={foto_ref}&key={API_KEY}"
                                st.image(foto_url, use_container_width=True)
                            else:
                                st.write("🖼️ Fotoğraf Yok")

                        with col_txt:
                            st.subheader(f"🏢 {isim}")
                            st.write(f"📍 **Adres:** {adres}")
                            if tel:
                                st.write(f"📞 **Telefon:** {tel}")
                            st.write(f"⏰ **Çalışma:** {calisma_saati} ({acik_mi_text})")
                            st.write(f"⭐ **Puan:** {puan}")
                        
                        b1, b2 = st.columns(2)
                        with b1:
                            h_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}&query_place_id={pid}"
                            st.link_button("📍 Yol Tarifi", h_link, use_container_width=True)
                        with b2:
                            if tel:
                                temiz_tel = "".join(filter(str.isdigit, tel))
                                if temiz_tel.startswith("0"): temiz_tel = "9" + temiz_tel
                                elif not temiz_tel.startswith("90"): temiz_tel = "90" + temiz_tel
                                
                                wa_link = f"https://wa.me/{temiz_tel}?text=Merhaba, {arama_terimi} fiyatı alabilir miyim?"
                                st.link_button("💬 WhatsApp'tan Fiyat Sor", wa_link, type="primary", use_container_width=True)
                            else:
                                st.button("💬 No Yok", disabled=True, use_container_width=True)
                
                if bulunan_sayisi == 0:
                    st.warning("Seçtiğiniz kriterlere göre (örneğin sadece açık dükkanlar) sonuç bulunamadı.")
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen bir ürün/kategori seçin ve konum girin.")

st.caption("© 2025 enucuzuburada.com.tr")
