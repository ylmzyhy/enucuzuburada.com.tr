import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARIN
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. ÖZEL TASARIM (CSS)
st.markdown("""
<style>
    /* Başlıkları ve metinleri küçült */
    h3 { font-size: 1rem !important; font-weight: bold; margin-bottom: 2px; }
    p { font-size: 0.85rem !important; margin-bottom: 2px; line-height: 1.2; }
    
    /* Dükkan kutularını daha kompakt yap */
    .dukkan-kart {
        border: 1px solid #eee;
        padding: 10px;
        border-radius: 8px;
        background-color: #fdfdfd;
        margin-bottom: 10px;
    }
    
    /* Logo alanındaki boşlukları azalt */
    .stImage { text-align: center; margin-top: -30px; }
    
    /* Buton boyutlarını ayarla */
    .stButton > button { height: 35px; font-size: 0.8rem !important; }
</style>
""", unsafe_allow_all_html=True)

# 4. ÜST KISIM (KÜÇÜK LOGO)
c1, c2, c3 = st.columns([1.5, 1, 1.5])
with c2:
    try:
        # width=120 yaparak logoyu bayağı ufaltıyoruz
        st.image("logo.png", width=120) 
    except:
        st.title("🛒 En Ucuzu Burada")

# 5. FONKSİYONLAR
def dukkan_ara(urun, lokasyon):
    sorgu = f"{urun} {lokasyon}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}&key={API_KEY}&language=tr"
    response = requests.get(url).json()
    return response.get('results', [])

def telefon_bul(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number&key={API_KEY}&language=tr"
    res = requests.get(url).json()
    return res.get('result', {}).get('formatted_phone_number', '')

# 6. ARAMA ALANI
st.write("") # Küçük boşluk
col_arama, col_yer = st.columns([2, 1])
with col_arama:
    arama = st.text_input("Ürün", placeholder="Ne arıyorsun?", label_visibility="collapsed")
with col_yer:
    yer = st.text_input("Konum", value="İstoç", label_visibility="collapsed")

ara_btn = st.button("Dükkanları Listele", use_container_width=True)

# 7. SONUÇLAR (GRID)
if ara_btn:
    if arama:
        with st.spinner('Aranıyor...'):
            sonuclar = dukkan_ara(arama, yer)
            if sonuclar:
                # Satırda 2 dükkan yan yana gelecek şekilde
                for i in range(0, len(sonuclar), 2):
                    cols = st.columns(2)
                    for j in range(2):
                        if i + j < len(sonuclar):
                            dukkan = sonuclar[i+j]
                            isim = dukkan.get('name')
                            adres = dukkan.get('formatted_address')[:50] + "..."
                            puan = dukkan.get('rating', 'Yok')
                            place_id = dukkan.get('place_id')
                            
                            with cols[j]:
                                st.markdown(f"""
                                <div class="dukkan-kart">
                                    <h3>🏢 {isim}</h3>
                                    <p>📍 {adres}</p>
                                    <p>⭐ Puan: {puan}</p>
                                </div>
                                """, unsafe_allow_all_html=True)
                                
                                b1, b2 = st.columns(2)
                                with b1:
                                    st.link_button("📍 Konum", f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}&query_place_id={place_id}", use_container_width=True)
                                with b2:
                                    tel = telefon_bul(place_id)
                                    if tel:
                                        wa_link = f"https://wa.me/{tel.replace(' ', '').replace('+', '')}"
                                        st.link_button("💬 WhatsApp", wa_link, use_container_width=True)
                                    else:
                                        st.button("📞 No Yok", disabled=True, use_container_width=True)
            else:
                st.warning("Sonuç bulunamadı.")
