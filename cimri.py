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
    # Telefon ve Detaylı Çalışma Saatlerini (weekday_text) çekmek için detay sorgusu
    fields = "formatted_phone_number,opening_hours,international_phone_number"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={API_KEY}&language=tr"
    res = requests.get(url).json()
    return res.get('result', {})

# 5. ARAMA ARAYÜZÜ
st.write("---")
c1, c2 = st.columns([2, 1])

with c1:
    arama = st.text_input("Ne arıyorsunuz?", placeholder="Örn: Kaynak Makinesi, Matkap...")

with c2:
    yer = st.text_input("Şehir / İlçe seçin", placeholder="Örn: Ankara Ostim, İstanbul İkitelli...")

if st.button("Dükkanları ve Fiyat Sorulacak Yerleri Bul", use_container_width=True):
    if arama and yer:
        with st.spinner('Bilgiler hazırlanıyor...'):
            sonuclar = dukkan_ara(arama, yer)
            
            if sonuclar:
                st.success(f"'{yer}' bölgesinde {len(sonuclar)} yer bulundu.")
                
                for dukkan in sonuclar:
                    isim = dukkan.get('name')
                    adres = dukkan.get('formatted_address')
                    puan = dukkan.get('rating', 'Yeni İşletme')
                    pid = dukkan.get('place_id')
                    
                    # Detayları (Telefon ve Saatler) çek
                    detay = detay_getir(pid)
                    tel = detay.get('formatted_phone_number') or detay.get('international_phone_number')
                    saatler = detay.get('opening_hours', {})
                    
                    # Çalışma Saatlerini Çözme
                    acik_mi_text = "Bilgi Yok"
                    calisma_saati = "Belirtilmemiş"
                    
                    if saatler:
                        # Şu an açık mı?
                        acik_mi_text = "✅ ŞİMDİ AÇIK" if saatler.get('open_now') else "❌ ŞİMDİ KAPALI"
                        
                        # Bugünün çalışma saatini al (weekday_text içinden)
                        # Not: weekday_text genellikle 7 günlük listeyi verir.
                        gunluk_liste = saatler.get('weekday_text', [])
                        if gunluk_liste:
                            # Bugünün hangi gün olduğunu bulup o satırı çekebiliriz
                            # Basitlik için tüm haftayı veya sadece bugünü gösterebiliriz.
                            # Burada dükkanın genel çalışma bilgisini gösteriyoruz.
                            calisma_saati = gunluk_liste[0].split(": ", 1)[-1] if gunluk_liste else "Belirtilmemiş"

                    with st.container():
                        st.divider()
                        st.subheader(f"🏢 {isim}")
                        st.write(f"📍 **Adres:** {adres}")
                        
                        # 1. Telefon
                        if tel:
                            st.write(f"📞 **Telefon:** {tel}")
                        else:
                            st.write("📞 **Telefon:** Belirtilmemiş")
                        
                        # 2. Açılış - Kapanış Saatleri
                        st.write(f"⏰ **Çalışma Saatleri:** {calisma_saati}")
                        st.write(f"ℹ️ **Durum:** {acik_mi_text}")
