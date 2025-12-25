import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="En Ucuzu Burada", page_icon="🛒", layout="wide")

# 2. API ANAHTARI
API_KEY = "AIzaSyDF9hKdF-D7atJJDqV-h56wlB7vgt9eqJE"

# 3. LOGO (SOLA YASLI VE BÜYÜK)
# Tasarım değişikliği sadece burada: Sola yaslamak için kolon yapısı kullanıldı
col_logo, col_bosluk = st.columns([1, 2]) 
with col_logo:
    try:
        # Genişlik 400px yapılarak logo büyütüldü
        st.image("logo.png", width=400) 
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

# 5. ARAMA ARAYÜZÜ (BOŞLUKLAR AZALTILDI)
# Logo ile arama arasındaki '---' kaldırıldı, dikey boşluk azaldı
c1, c2 = st.columns([2, 1], gap="small")

with c1:
    arama = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Kaynak Makinesi, Matkap...", key="search_input_safe")

with c2:
    yer = st.text_input("Şehir / İlçe seçin", placeholder="Örn: Ankara Ostim, İkitelli...", key="loc_input_safe")

# Arama Butonu
if st.button("Dükkanları ve Fiyat Sorulacak Yerleri Bul", use_container_width=True, key="main_search_btn"):
    if arama and yer:
        with st.spinner('Detaylı bilgiler çekiliyor...'):
            sonuclar = dukkan_ara(arama, yer)
            
            if sonuclar:
                st.success(f"'{yer}' bölgesinde {len(sonuclar)} yer bulundu.")
                
                for idx, dukkan in enumerate(sonuclar):
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    puan = dukkan.get('rating', 'Yeni İşletme')
                    pid = dukkan.get('place_id')
                    
                    detay = detay_getir(pid)
                    tel = detay.get('formatted_phone_number') or detay.get('international_phone_number')
                    saatler = detay.get('opening_hours', {})
                    fotolar = detay.get('photos', [])
                    
                    acik_mi_text = "Bilgi Yok"
                    if saatler:
                        acik_mi_text = "✅ ŞİMDİ AÇIK" if saatler.get('open_now') else "❌ ŞİMDİ KAPALI"

                    # DÜKKAN KARTI (Kutucuklu kurumsal yapı)
                    with st.container(border=True):
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
                            st.write(f"⭐ **Puan:** {puan} | {acik_mi_text}")
                        
                        # Butonlar (Hata almamak için benzersiz anahtarlar eklendi)
                        b1, b2 = st.columns(2)
                        with b1:
                            harita_link = f"https://www.google.com/maps/search/?api=1&query={isim.replace(' ', '+')}&query_place_id={pid}"
                            st.link_button("📍 Konum", harita_link, use_container_width=True, key=f"btn_map_{idx}_{pid}")
                        
                        with b2:
                            if tel:
                                temiz_tel = "".join(filter(str.isdigit, tel))
                                if temiz_tel.startswith("0"):
                                    temiz_tel = "9" + temiz_tel
                                elif not temiz_tel.startswith("90"):
                                    temiz_tel = "90" + temiz_tel 
                                
                                wa_mesaj = f"Merhaba, {arama} ürünü için fiyat bilgisi alabilir miyim?"
                                wa_link = f"https://wa.me/{temiz_tel}?text={wa_mesaj}"
                                st.link_button("💬 WhatsApp", wa_link, type="primary", use_container_width=True, key=f"btn_wa_{idx}_{pid}")
                            else:
                                st.button("💬 No Yok", disabled=True, use_container_width=True, key=f"btn_none_{idx}_{pid}")
            else:
                st.warning("Sonuç bulunamadı.")
    else:
        st.error("Lütfen tüm alanları doldurun.")

st.caption("© 2025 enucuzuburada.com.tr")
