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

# 5. DEV KATEGORİ MENÜSÜ (Trendyol Tarzı)
st.write("---")
st.markdown("### 🏬 Alışveriş Kategorileri")

# Kategorileri gruplara ayırıyoruz
kat_gruplari = {
    "📱 Elektronik": ["Cep Telefonu", "Bilgisayar", "Tablet", "Televizyon", "Kamera", "Beyaz Eşya"],
    "🏠 Ev & Yaşam": ["Mobilya", "Dekorasyon", "Mutfak Gereçleri", "Aydınlatma", "Ev Tekstili"],
    "🛠️ Yapı & Sanayi": ["Hırdavat", "İnşaat Malzemesi", "Elektrik Malzemesi", "Ambalaj", "İş Güvenliği"],
    "🏎️ Oto & Motosiklet": ["Oto Aksesuar", "Lastik", "Motosiklet Parça", "Oto Bakım"],
    "🧸 Anne & Çocuk": ["Oyuncak", "Bebek Bakım", "Çocuk Giyim", "Okul Malzemeleri"],
    "💄 Kozmetik & Sağlık": ["Parfüm", "Cilt Bakımı", "Medikal Ürünler", "Kişisel Bakım"]
}

secilen_kategori = ""

# Kategorileri şık bir şekilde listeleme
for grup_ismi, liste in kat_gruplari.items():
    with st.expander(grup_ismi):
        # Her gruptaki öğeleri yan yana dizmek için kolonlar
        cols = st.columns(len(liste))
        for i, kat in enumerate(liste):
            if cols[i].button(kat, key=f"kat_{kat}", use_container_width=True):
                secilen_kategori = kat

st.write("") 

# 6. ARAMA ARAYÜZÜ
c1, c2 = st.columns([2, 1])
with c1:
    arama_input = st.text_input("Ne arıyorsunuz?", value=secilen_kategori, placeholder="Marka, ürün veya dükkan adı...")
with c2:
    yer = st.text_input("Şehir / İlçe", value="İstoç", placeholder="Nerede arayalım?")

sadece_acik = st.toggle("Sadece şu an açık olanları göster")

# 7. ARAMA MANTIĞI
if st.button("Dükkanları Listele", use_container_width=True) or (secilen_kategori != ""):
    final_arama = arama_input if arama_input else secilen_kategori
    
    if final_arama and yer:
        with st.spinner('Sonuçlar taranıyor...'):
            sonuclar = dukkan_ara(final_arama, yer)
            
            if sonuclar:
                # Puanı yüksek olanları en başa alalım (Küçük bir sıralama zekası)
                sonuclar = sorted(sonuclar, key=lambda x: x.get('rating', 0), reverse=True)
                
                bulunan_sayisi = 0
                for dukkan in sonuclar:
                    pid = dukkan.get('place_id')
                    detay = detay_getir(pid)
                    saatler = detay.get('opening_hours', {})
                    su_an_acik = saatler.get('open_now', False) if saatler else False
                    
                    if sadece_acik and not su_an_acik:
                        continue 
                    
                    bulunan_sayisi += 1
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    puan = dukkan.get('rating', 'Yeni')
                    tel = detay.get('formatted_phone_number') or detay.get('international_phone_number')
                    fotolar = detay.get('photos', [])
                    
                    acik_mi_text = "✅ AÇIK" if su_an_acik else "❌ KAPALI"
                    
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
                            st.subheader(f"🏢 {isim}")
                            st.write(f"📍 {adres}")
                            if tel: st.write(f"📞 **Telefon:** {tel}")
                            st.write(f"⭐ **Puan:** {puan} | **Durum:** {acik_mi_text}")
                        
                        b1, b2 = st.columns(2)
                        with b1:
                            h_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}&query_place_id={pid}"
                            st.link_button("📍 Konum", h_link, use_container_width=True)
                        with b2:
                            if tel:
                                temiz_tel = "".join(filter(str.isdigit, tel))
                                if temiz_tel.startswith("0"): temiz_tel = "9" + temiz_tel
                                elif not temiz_tel.startswith("90"): temiz_tel = "90" + temiz_tel
                                
                                wa_link = f"https://wa.me/{temiz_tel}?text=Merhaba, {final_arama} için fiyat alabilir miyim?"
                                st.link_button("💬 WhatsApp Fiyat Sor", wa_link, type="primary", use_container_width=True)
                            else:
                                st.button("💬 No Bulunamadı", disabled=True, use_container_width=True)
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen arama kutusunu ve konumu doldurun.")

st.caption("© 2025 enucuzuburada.com.tr | Türkiye'nin En Kapsamlı Rehberi")
