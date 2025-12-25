import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARI
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO VE BAŞLIK
st.title("🛒 En Ucuzu Burada")
st.write("Dükkanları bulun ve hızlıca fiyat sorun.")

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
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={pid}&fields=formatted_phone_number,photos,opening_hours&key={API_KEY}&language=tr"
    try:
        r = requests.get(url).json()
        return r.get('result', {})
    except:
        return {}

# 5. ARAMA BÖLÜMÜ
col_a, col_b = st.columns([2, 1])
with col_a:
    input_ara = st.text_input("Ürün veya Marka", placeholder="Örn: Cep Telefonu, Matkap...", key="q")
with col_b:
    input_yer = st.text_input("Konum", value="İstanbul", key="l")

if st.button("Dükkanları Listele", use_container_width=True, type="primary"):
    if input_ara and input_yer:
        with st.spinner('Sonuçlar taranıyor...'):
            sonuclar = dukkan_ara(input_ara, input_yer)
            
            if sonuclar:
                for idx, dukkan in enumerate(sonuclar):
                    pid = dukkan.get('place_id')
                    detay = detay_getir(pid)
                    
                    isim = dukkan.get('name', 'İsimsiz İşletme')
                    adres = dukkan.get('formatted_address', 'Adres yok')
                    tel = detay.get('formatted_phone_number')
                    fotolar = detay.get('photos', [])
                    
                    with st.container():
                        st.divider()
                        c1, c2 = st.columns([1, 3])
                        
                        with c1:
                            if fotolar:
                                f_ref = fotolar[0].get('photo_reference')
                                f_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={f_ref}&key={API_KEY}"
                                st.image(f_url, use_container_width=True)
                            else:
                                st.write("🖼️ Görsel Yok")
                        
                        with c2:
                            st.subheader(isim)
                            st.write(f"📍 {adres}")
                            if tel: st.write(f"📞 **Telefon:** {tel}")
                            
                            # Butonlar için benzersiz key ataması
                            b_col1, b_col2 = st.columns(2)
                            with b_col1:
                                m_url = f"https://www.google.com/maps/search/?api=1&query={isim}&query_place_id={pid}"
                                st.link_button("📍 Haritada Gör", m_url, use_container_width=True, key=f"map_{idx}")
                            
                            with b_col2:
                                if tel:
                                    t_clean = "".join(filter(str.isdigit, tel))
                                    if t_clean.startswith("0"): t_clean = "9" + t_clean
                                    elif not t_clean.startswith("90"): t_clean = "90" + t_clean
                                    
                                    w_url = f"https://wa.me/{t_clean}?text=Merhaba, {input_ara} fiyatı alabilir miyim?"
                                    st.link_button("💬 WhatsApp", w_url, use_container_width=True, key=f"wa_{idx}")
                                else:
                                    st.button("📞 Telefon Yok", disabled=True, use_container_width=True, key=f"no_{idx}")
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen tüm alanları doldurun.")

st.caption("© 2025 enucuzuburada.com.tr")
