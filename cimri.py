import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARIN
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. ÖZEL TASARIM (Görseli Ufaltan ve Sıkılaştıran CSS)
st.markdown("""
<style>
    /* Logo ve üst boşluğu daralt */
    .stImage { text-align: center; margin-top: -40px; margin-bottom: -20px; }
    
    /* Başlık ve yazıları kibarlaştır */
    h3 { font-size: 0.95rem !important; font-weight: bold; margin-bottom: 2px; color: #1E1E1E; }
    p { font-size: 0.8rem !important; margin-bottom: 2px; color: #555; }
    
    /* Dükkan kutularını (Card) küçült */
    .dukkan-kart {
        border: 1px solid #f0f0f0;
        padding: 8px;
        border-radius: 10px;
        background-color: #ffffff;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Butonları daha ince yap */
    .stButton > button { height: 32px; font-size: 0.75rem !important; border-radius: 6px; }
</style>
""", unsafe_allow_all_html=True)

# 4. ÜST KISIM (KİBAR LOGO)
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    try:
        # width=100 yaparak logoyu tam istediğin gibi ufaltıyoruz
        st.image("logo.png", width=100) 
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
st.write("") 
c_ara, c_yer = st.columns([2, 1])
with c_ara:
    arama = st.text_input("Ürün", placeholder="Ne arıyorsun?", label_visibility="collapsed")
with c_yer:
    yer = st.text_input("Konum", value="İstoç", label_visibility="collapsed")

if st.button("Dükkanları Listele", use_container_width=True):
    if arama:
        with st.spinner('Sonuçlar geliyor...'):
            sonuclar = dukkan_ara(arama, yer)
            if sonuclar:
                st.success(f"{len(sonuclar)} dükkan bulundu.")
                # Izgara (Grid) görünümü: Yan yana 2 dükkan
                for i in range(0, len(sonuclar), 2):
                    cols = st.columns(2)
                    for j in range(2):
                        if i + j < len(sonuclar):
                            dukkan = sonuclar[i+j]
                            isim = dukkan.get('name')
                            adres = dukkan.get('formatted_address', '')[:45] + "..."
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
                                    st.link_button("📍 Konum", f"https://www.google.com/maps/place/?q=place_id:{place_id}", use_container_width=True)
                                with b2:
                                    tel = telefon_bul(place_id)
                                    if tel:
                                        wa_link = f"https://wa.me/{tel.replace(' ', '').replace('+', '')}?text=Merhaba,{arama} fiyatı alabilir miyim?"
                                        st.link_button("💬 WhatsApp", wa_link, use_container_width=True)
                                    else:
                                        st.button("📞 No Yok", disabled=True, use_container_width=True)
            else:
                st.warning("Sonuç bulunamadı.")
