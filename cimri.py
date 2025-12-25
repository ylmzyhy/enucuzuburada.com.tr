import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARI
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO (SOLA YASLI VE BÜYÜK)
col_logo, col_bosluk = st.columns([1, 2]) 
with col_logo:
    try:
        st.image("logo.png", width=400) 
    except:
        st.title("🛒 En Ucuzu Burada")

# 4. FONKSİYONLAR
def dukkan_ara(urun, lokasyon):
    sorgu = f"{urun} {lokasyon}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}&key={API_KEY}&language=tr"
    try:
        response = requests.get(url).json()
        return response.get('results', [])
    except:
        return []

def detay_getir(place_id):
    fields = "formatted_phone_number,opening_hours,international_phone_number,photos"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={API_KEY}&language=tr"
    try:
        res = requests.get(url).json()
        return res.get('result', {})
    except:
        return {}

# 5. KURUMSAL ARAMA ARAYÜZÜ (Cimri.com Stili)
st.write("")
# Kategoriler için modern bir seçim alanı
kategoriler = ["Tümü", "Hırdavat", "Elektronik", "Yapı Market", "Mobilya", "Beyaz Eşya"]
secilen_kategori = st.pills("Popüler Kategoriler", kategoriler, selection_mode="single", default="Tümü")

# Arama Çubuğu Tasarımı
c1, c2 = st.columns([3, 1], gap="small")
with c1:
    # Kategori seçilmişse arama kutusuna otomatik yazar
    varsayilan_arama = "" if secilen_kategori == "Tümü" else secilen_kategori
    arama = st.text_input("Neyi en ucuza almak istersin?", value=varsayilan_arama, placeholder="Ürün, marka veya dükkan ara...")
with c2:
    yer = st.text_input("Konum seçin", value="İstanbul", placeholder="Şehir veya İlçe...")

search_clicked = st.button("Dükkanları ve Fiyatları Bul", use_container_width=True, type="primary")

# 6. SONUÇLAR VE KART TASARIMI
if search_clicked or (secilen_kategori != "Tümü" and not arama):
    arama_terimi = arama if arama else secilen_kategori
    if arama_terimi and yer:
        with st.spinner('En uygun dükkanlar taranıyor...'):
            sonuclar = dukkan_ara(arama_terimi, yer)
            
            if sonuclar:
                st.subheader(f"🔍 {arama_terimi} için sonuçlar ({len(sonuclar)} dükkan)")
                
                for idx, dukkan in enumerate(sonuclar):
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    puan = dukkan.get('rating', 'Yeni')
                    pid = dukkan.get('place_id')
                    
                    detay = detay_getir(pid)
                    tel = detay.get('formatted_phone_number') or detay.get('international_phone_number')
                    saatler = detay.get('opening_hours', {})
                    fotolar = detay.get('photos', [])
                    
                    acik_mi = "✅ AÇIK" if saatler.get('open_now') else "❌ KAPALI"
                    
                    # KURUMSAL KART TASARIMI
                    with st.container(border=True): # Çerçeveli kart yapısı
                        col_img, col_txt = st.columns([1, 3])
                        
                        with col_img:
                            if fotolar:
                                f_ref = fotolar[0].get('photo_reference')
                                f_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={f_ref}&key={API_KEY}"
                                st.image(f_url, use_container_width=True)
                            else:
                                st.image("https://via.placeholder.com/400x300?text=Gorsel+Yok", use_container_width=True)

                        with col_txt:
                            st.markdown(f"### {isim}")
                            st.caption(f"📍 {adres}")
                            
                            st.write(f"⭐ **Puan:** {puan} | {acik_mi}")
                            
                            # Butonlar için özel ID ataması (Hata önleyici)
                            b1, b2 = st.columns(2)
                            with b1:
                                m_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}&query_place_id={pid}"
                                st.link_button("📍 Haritada Gör", m_link, use_container_width=True, key=f"map_{pid}_{idx}")
                            
                            with b2:
                                if tel:
                                    t_clean = "".join(filter(str.isdigit, tel))
                                    if t_clean.startswith("0"): t_clean = "9" + t_clean
                                    elif not t_clean.startswith("90"): t_clean = "90" + t_clean
                                    
                                    w_link = f"https://wa.me/{t_clean}?text=Merhaba, {arama_terimi} fiyatı alabilir miyim?"
                                    st.link_button("💬 WhatsApp'tan Sor", w_link, type="primary", use_container_width=True, key=f"wa_{pid}_{idx}")
                                else:
                                    st.button("📞 No Mevcut Değil", disabled=True, use_container_width=True, key=f"no_{pid}_{idx}")
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen arama terimi ve konum girin.")

st.divider()
st.caption("© 2025 enucuzuburada.com.tr | Kurumsal Rehber")
