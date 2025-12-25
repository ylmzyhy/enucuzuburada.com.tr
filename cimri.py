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
    # Fotoğraf, Telefon ve Saatler için detay sorgusu
    fields = "formatted_phone_number,opening_hours,international_phone_number,photos"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={API_KEY}&language=tr"
    res = requests.get(url).json()
    return res.get('result', {})

# 5. ARAMA ARAYÜZÜ
st.write("---")
c1, c2 = st.columns([2, 1])

with c1:
    arama = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Kaynak Makinesi, Matkap...")

with c2:
    yer = st.text_input("Şehir / İlçe seçin", placeholder="Örn: Ankara Ostim, İkitelli...")

if st.button("Dükkanları ve Fiyat Sorulacak Yerleri Bul", use_container_width=True):
    if arama and yer:
        with st.spinner('Detaylı bilgiler çekiliyor...'):
            sonuclar = dukkan_ara(arama, yer)
            
            if sonuclar:
                st.success(f"'{yer}' bölgesinde {len(sonuclar)} yer bulundu.")
                
                for dukkan in sonuclar:
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    puan = dukkan.get('rating', 'Yeni İşletme')
                    pid = dukkan.get('place_id')
                    
                    # Detayları (Telefon, Saat, Foto) çek
                    detay = detay_getir(pid)
                    tel = detay.get('formatted_phone_number') or detay.get('international_phone_number')
                    saatler = detay.get('opening_hours', {})
                    fotolar = detay.get('photos', [])
                    
                    acik_mi_text = "Bilgi Yok"
                    calisma_saati = "Belirtilmemiş"
                    
                    if saatler:
                        acik_mi_text = "✅ ŞİMDİ AÇIK" if saatler.get('open_now') else "❌ ŞİMDİ KAPALI"
                        gunluk_liste = saatler.get('weekday_text', [])
                        if gunluk_liste:
                            calisma_saati = gunluk_liste[0].split(": ", 1)[-1]

                    with st.container():
                        st.divider()
                        # Görsel ve Metni yan yana getirmek için kolonlar
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
                            st.write(f"⏰ **Çalışma Saatleri:** {calisma_saati} ({acik_mi_text})")
                            st.write(f"⭐ **Puan:** {puan}")
                        
                        # Butonlar
                        b1, b2 = st.columns(2)
                        with b1:
                            harita_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}&query_place_id={pid}"
                            st.link_button("📍 Konum / Yol Tarifi", harita_link, use_container_width=True)
                        
                        with b2:
                            if tel:
                                temiz_tel = "".join(filter(str.isdigit, tel))
                                if temiz_tel.startswith("0"):
                                    temiz_tel = "9" + temiz_tel
                                elif not temiz_tel.startswith("90"):
                                    temiz_tel = "90" + temiz_tel # Türkiye kodu eklemesi
                                
                                wa_mesaj = f"Merhaba, {arama} ürünü için fiyat bilgisi alabilir miyim?"
                                wa_link = f"https://wa.me/{temiz_tel}?text={wa_mesaj}"
                                st.link_button("💬 WhatsApp'tan Fiyat Sor", wa_link, type="primary", use_container_width=True)
                            else:
                                st.button("💬 No Mevcut Değil", disabled=True, use_container_width=True)
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen tüm alanları doldurun.")

st.caption("© 2025 enucuzuburada.com.tr")
