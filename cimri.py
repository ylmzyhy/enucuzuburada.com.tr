import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARIN
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. ÖZEL TASARIM (Hatalardan Arındırılmış Temiz CSS)
st.markdown("""
<style>
    /* Üst boşlukları ve logoyu düzenle */
    .stImage { text-align: center; margin-top: -30px; }
    
    /* Yazı tiplerini ve boyutlarını küçült */
    h3 { font-size: 1.1rem !important; font-weight: bold; margin-bottom: 5px; color: #333; }
    p { font-size: 0.9rem !important; margin-bottom: 2px; }
    
    /* Dükkan kutularını (Card) özelleştir */
    .dukkan-kart {
        border: 1px solid #eee;
        padding: 12px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_all_html=True)

# 4. ÜST KISIM (KÜÇÜK LOGO)
c1, c2, c3 = st.columns([1.5, 1, 1.5])
with c2:
    try:
        st.image("logo.png", width=100) # Logo boyutunu tam istediğin gibi ufaltıyoruz
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
col_arama, col_yer = st.columns([2, 1])
with col_arama:
    arama = st.text_input("Ürün", placeholder="Ne arıyorsun?", label_visibility="collapsed")
with col_yer:
    yer = st.text_input("Konum", value="İstoç", label_visibility="collapsed")

if st.button("Dükkanları Listele", use_container_width=True):
    if arama:
        with st.spinner('Sonuçlar yükleniyor...'):
            sonuclar = dukkan_ara(arama, yer)
            if sonuclar:
                st.success(f"{yer} bölgesinde {len(sonuclar)} dükkan bulundu.")
                # Her satırda 2 dükkan gösterecek grid yapısı
                for i in range(0, len(sonuclar), 2):
                    cols = st.columns(2)
                    for j in range(2):
                        if i + j < len(sonuclar):
                            dukkan = sonuclar[i+j]
                            isim = dukkan.get('name')
                            adres = dukkan.get('formatted_address', '')[:55] + "..."
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
                                    st.link_button("📍 Konum", f"google.com/maps/search?q={isim.replace(' ', '+')}&query_place_id={place_id}", use_container_width=True)
                                with b2:
                                    tel = telefon_bul(place_id)
                                    if tel:
                                        wa_link = f"https://wa.me/{tel.replace(' ', '').replace('+', '')}?text=Merhaba, {arama} fiyatı öğrenebilir miyim?"
                                        st.link_button("💬 WhatsApp", wa_link, use_container_width=True)
                                    else:
                                        st.button("📞 No Yok", disabled=True, use_container_width=True)
            else:
                st.warning("Sonuç bulunamadı.")

st.caption("© 2025 enucuzuburada.com.tr")
