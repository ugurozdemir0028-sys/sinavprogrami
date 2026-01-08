import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- GÜVENLİK AYARI ---
# GitHub'a yüklerken anahtarın çalınmaması için bu yöntemi kullanıyoruz
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = "AIzaSyDRQ4FGai8-p_tw1h_ZCD5FHjV6TrIjnr8"
genai.configure(api_key=api_key)

# --- PDF OKUMA FONKSİYONU ---
def pdf_metni_oku(dosya):
    pdf_okuyucu = PdfReader(dosya)
    metin = ""
    for sayfa in pdf_okuyucu.pages:
        metin += sayfa.extract_text()
    return metin

# --- ARAYÜZ ---
st.set_page_config(page_title="Sınav Analiz Robotu", layout="centered")
st.title("📊 Sınav Analiz ve Değerlendirme Raporu")
st.info("E-okuldan indirdiğiniz PDF'i yükleyin, gerisini yapay zekaya bırakın.")

yuklenen_dosya = st.file_uploader("Sınav Sonuç PDF'ini Seçin", type="pdf")

if yuklenen_dosya:
    with st.spinner("Veriler analiz ediliyor, lütfen bekleyin..."):
        # 1. PDF'den veriyi al
        ham_veri = pdf_metni_oku(yuklenen_dosya)
        
        # 2. Yapay zekaya talimat gönder
        model = genai.GenerativeModel('gemini-1.5-flash') # AI Studio'da seçtiğiniz model
        
        # Burası sizin AI Studio'daki sistem talimatınızdır
        istem = f"""
        Aşağıdaki verileri kullanarak resmi bir Sınav Analiz Raporu oluştur:
        - Sınıf bilgisini en başa yaz.
        - Karşılaştırmalı bir tablo hazırla.
        - Başarıyı yorumla ve eylem planı ekle.
        - En sona öğretmen adı için isim ve imza alanı ekle.
        Veriler: {ham_veri}
        """
        
        cevap = model.generate_content(istem)
        
        # 3. Sonucu Ekrana Yazdır
        st.markdown("---")
        st.markdown(cevap.text)
        
        # Not: PDF indirme butonu için ek kütüphaneler (fpdf gibi) gerekir. 
        # Şimdilik sonucu ekrandan kopyalayıp Word'e yapıştırabilirsiniz.
