import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARI
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO (SOLA YASLI VE BÜYÜK)
# Sadece tasarım yerleşimi için sütun kullanıldı
col_logo, col_bosluk = st.columns([1, 2]) 
with col_logo:
    try:
        st.image("logo.png", width=400) 
    except:
        st.title("En Ucuzu Burada")

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

# 5. ARAMA ARAYÜZÜ (BOŞLUKLAR AZALTILDI)
c1, c2 = st.columns([2, 1])

with c1:
    arama = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Matkap, Kaynak Makinesi...", key="search")

with c2:
    yer = st.text_input("Şehir / İlçe", placeholder="Örn: İstanbul İkitelli...", key="location")

if st.button("Dükkanları Bul", use_container_width=True, type="primary"):
    if arama and yer:
        with st.spinner('Sonuçlar yükleniyor...'):
            sonuclar = dukkan_ara(arama, yer)
            
            if sonuclar:
                for idx, dukkan in enumerate(sonuclar):
                    isim = dukkan.get('name', 'Bilinmeyen İşletme')
                    adres = dukkan.get('formatted_address', 'Adres yok')
                    pid = dukkan.get('place_id')
                    
                    detay = detay_getir(pid)
                    tel = detay.get('formatted_phone_number')
                    fotolar = detay.get('photos', [])
                    
                    # Sade Görünüm
                    st.markdown(f"### {isim}")
                    st.write(f"Adres: {adres}")
                    if tel:
                        st.write(f"Telefon: {tel}")
                    
                    # Butonlar için en basit key yapısı (Hata almamak için emoji kaldırıldı)
                    b1, b2 = st.columns(2)
                    with b1:
                        m_url = f"https://www.google.com/maps/search/?api=1&query={isim}&query_place_id={pid}"
                        st.link_button("Haritada Gor", m_url, use_container_width=True, key=f"m{idx}")
                    
                    with b2:
                        if tel:
                            t_clean = "".join(filter(str.isdigit, tel))
                            if t_clean.startswith("0"): t_clean = "9" + t_clean
                            elif not t_clean.startswith("90"): t_clean = "90" + t_clean
                            
                            w_url = f"https://wa.me/{t_clean}?text=Merhaba,{arama}fiyatini_ogrenebilirmiyim?"
                            st.link_button("WhatsApp Fiyat Sor", w_url, use_container_width=True, key=f"w{idx}")
                        else:
                            st.button("Telefon Yok", disabled=True, use_container_width=True, key=f"n{idx}")
                    st.divider()
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen alanları doldurun.")

st.caption("© 2025 enucuzuburada.com.tr")
