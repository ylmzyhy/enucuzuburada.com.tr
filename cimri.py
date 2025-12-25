import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARI
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO (Boyutu dengelendi)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    try:
        st.image("logo.png", width=220)
    except:
        st.title("🛒 En Ucuzu Burada")

# 4. FONKSİYONLAR
def dukkan_ara(urun, lokasyon):
    # Lokasyonu sorguya ekleyerek tüm illerde arama yapmasını sağlıyoruz
    sorgu = f"{urun} {lokasyon}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={sorgu}&key={API_KEY}&language=tr"
    response = requests.get(url).json()
    return response.get('results', [])

def telefon_getir(place_id):
    # Telefon numarasını çekmek için özel 'details' sorgusu
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number,international_phone_number&key={API_KEY}&language=tr"
    res = requests.get(url).json()
    result = res.get('result', {})
    # Hem yerel hem uluslararası formatı kontrol et
    return result.get('formatted_phone_number') or result.get('international_phone_number')

# 5. ARAMA ARAYÜZÜ
st.write("---")
c1, c2 = st.columns([2, 1])

with c1:
    arama = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Kaynak Makinesi, Matkap, Vida...")

with c2:
    yer = st.text_input("Şehir / İlçe / Sanayi Sitesi", placeholder="Örn: Ankara Ostim, İzmir, Konya...")

if st.button("Dükkanları ve Fiyat Sorulacak Yerleri Bul", use_container_width=True):
    if arama and yer:
        with st.spinner(f'{yer} bölgesinde {arama} satan yerler taranıyor...'):
            sonuclar = dukkan_ara(arama, yer)
            
            if sonuclar:
                st.success(f"'{yer}' bölgesinde {len(sonuclar)} dükkan/işletme bulundu.")
                
                for dukkan in sonuclar:
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    puan = dukkan.get('rating', 'Yeni İşletme')
                    pid = dukkan.get('place_id')
                    
                    with st.container():
                        st.divider()
                        st.subheader(f"🏢 {isim}")
                        st.write(f"📍 **Adres:** {adres}")
                        st.write(f"⭐ **Puan:** {puan}")
                        
                        col_btn1, col_btn2 = st.columns(2)
                        
                        with col_btn1:
                            # Google Haritalar Konum Linki
                            harita_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}&query_place_id={pid}"
                            st.link_button("📍 Haritada Gör / Yol Tarifi", harita_link, use_container_width=True)
                        
                        with col_btn2:
                            # Telefonu sorgula ve WhatsApp butonu oluştur
                            tel = telefon_getir(pid)
                            if tel:
                                # Telefon numarasını temizle (sadece rakam bırak)
                                temiz_tel = "".join(filter(str.isdigit, tel))
                                # Eğer numara 0 ile başlıyorsa (Türkiye için) 9 ekleyebiliriz
                                if temiz_tel.startswith("0"):
                                    temiz_tel = "9" + temiz_tel
                                
                                wa_mesaj = f"Merhaba, {arama} ürünü için fiyat bilgisi alabilir miyim?"
                                wa_link = f"https://wa.me/{temiz_tel}?text={wa_mesaj}"
                                st.link_button("💬 WhatsApp'tan Fiyat Sor", wa_link, type="primary", use_container_width=True)
                            else:
                                st.warning("📞 Telefon/WhatsApp Bulunamadı")
            else:
                st.warning(f"Üzgünüz, '{yer}' bölgesinde uygun bir yer bulunamadı. Lütfen daha genel bir konum deneyin (Örn: Sadece şehir ismi).")
    else:
        st.error("Lütfen hem ürün adını hem de konumu doldurun.")

st.caption("© 2025 enucuzuburada.com.tr | Türkiye'nin Tüm Sanayi ve Ticaret Merkezleri")
