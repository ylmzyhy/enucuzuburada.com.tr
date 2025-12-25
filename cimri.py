import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARIN
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. ÖZEL TASARIM (CSS) - Her şeyi derli toplu yapar
st.markdown("""
<style>
    /* Ana başlık ve yazı boyutlarını küçült */
    h3 { font-size: 1.1rem !important; font-weight: bold; color: #333; margin-bottom: 5px; }
    p { font-size: 0.9rem !important; margin-bottom: 2px; }
    
    /* Dükkan kutularını (Card) özelleştir */
    .dukkan-kart {
        border: 1px solid #eee;
        padding: 15px;
        border-radius: 12px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        height: 100%;
        transition: 0.3s;
    }
    .dukkan-kart:hover { border-color: #f39233; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    
    /* Arama çubuğu alanını daralt */
    .stTextInput > div > div > input { padding: 8px; }
</style>
""", unsafe_allow_all_html=True)

# 4. ÜST KISIM (LOGO)
c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    try:
        st.image("logo.png", width=180) # Logo boyutunu biraz küçülttük
    except:
        st.title("En Ucuzu Burada")

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

# 6. ARAMA ALANI (Daha kompakt)
with st.container():
    col_arama, col_yer = st.columns([2, 1])
    with col_arama:
        arama = st.text_input("Ürün adı", placeholder="Matkap, Vida...", label_visibility="collapsed")
    with col_yer:
        yer = st.text_input("Konum", value="İstoç", label_visibility="collapsed")
    
    ara_btn = st.button("Dükkanları Listele", use_container_width=True)

# 7. SONUÇLARI GÖSTER (Grid / Yan yana yapı)
if ara_btn:
    if arama:
        with st.spinner('Sonuçlar yükleniyor...'):
            sonuclar = dukkan_ara(arama, yer)
            if sonuclar:
                st.success(f"{len(sonuclar)} dükkan listelendi.")
                
                # Her satırda 2 veya 3 dükkan göstermek için döngü
                for i in range(0, len(sonuclar), 2):
                    cols = st.columns(2) # Satırda 2 dükkan yan yana
                    for j in range(2):
                        if i + j < len(sonuclar):
                            dukkan = sonuclar[i+j]
                            isim = dukkan.get('name')
                            adres = dukkan.get('formatted_address')[:60] + "..." # Adresi kısalttık
                            puan = dukkan.get('rating', 'Yok')
                            place_id = dukkan.get('place_id')
                            
                            with cols[j]:
                                # Kart yapısını başlat
                                st.markdown(f"""
                                <div class="dukkan-kart">
                                    <h3>🏢 {isim}</h3>
                                    <p>📍 {adres}</p>
                                    <p>⭐ Puan: {puan}</p>
                                </div>
                                """, unsafe_allow_all_html=True)
                                
                                # Butonlar (Streamlit'in kendi butonlarını kartın altına koyuyoruz)
                                b1, b2 = st.columns(2)
                                with b1
