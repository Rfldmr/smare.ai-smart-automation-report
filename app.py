import streamlit as st
import joblib
import numpy as np
from fpdf import FPDF
from datetime import datetime
import time

model = joblib.load('Model/smare_model.pkl')


st.sidebar.title("📄 SMARE.AI - v.1.0.25")
st.sidebar.markdown("")
st.sidebar.warning("SMARE.AI **tidak dirancang** untuk menyimpan data yang diinput oleh pengguna, menjamin sistem bebas dari kemungkinan pencurian data.")

st.sidebar.markdown("")

st.sidebar.markdown("""
    **Cara Penggunaan :**
    1. Pelajari SOP pengambilan dan pengujian kualitas air.
    2. Masukkan data yang diperlukan.
    3. Klik "Buat Laporan" untuk memproses laporan.
    4. Tekan tombol unduh untuk menyimpan laporan dalam pdf.
""")

st.sidebar.markdown("---")

st.sidebar.markdown("""
    - **Pengembang:** Rafli Damara  
    - **Versi:** 1.0.25
""")


st.title("Selamat Datang Di SMARE.AI! 👋")
st.subheader("Smart Automation Report for Certification.")
st.markdown("")
st.markdown("SMARE.AI merupakan sebuah tools yang memungkinkan perusahaan pengujian kualitas air membuat laporan mereka secara otomatis dengan memasukan berbagai data yang dibutuhkan dalam sebuah form. Selain itu, SMARE.AI juga didukung oleh model AI yang dapat memutuskan layak atau tidaknya kualitas air untuk dikonsumsi secara otomatis yang akan disampaikan sebagai kesimpulan dari laporan.")
st.markdown("")
st.info('Pelajari prosedur pengambilan dan pengujian kualitas air minum [**disini**](https://www.indonesian-publichealth.com/prosedur-pengambilan-dan-pengujian-kualitas-air-minum/)', icon="🔍")

st.markdown("")
st.divider()

st.subheader("Data Administratif")
st.markdown("")

nomor_pengujian = st.text_input("**Nomor Pengujian**")
nama_pelanggan = st.text_input("**Nama Pelanggan**")
alamat_pelanggan = st.text_input("**Alamat Pelanggan**")
tanggal_ambil_sample = st.date_input("**Tanggal Ambil Sampel**")
lokasi_ambil_sample = st.text_input("**Lokasi Ambil Sampel**")
tanggal_analisa = st.date_input("**Tanggal Analisa**")

st.divider()

st.subheader("Data Hasil Uji")
st.markdown("")

features = ["ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"]
input_values = []
metode_pengujian = []

for feature in features:
    col1, col2 = st.columns(2)
    with col1:
        input_value = st.number_input(f"**Masukan Nilai {feature}**", value=0.0)
        input_values.append(input_value)
    with col2:
        metode = st.text_input(f"**Metode Pengujian {feature}**")
        metode_pengujian.append(metode)
        
            
st.divider()

st.subheader("Data Penanggung Jawab")
st.markdown("")

penanggung_jawab = st.text_input("**Nama Penanggung Jawab**")
jabatan = st.text_input("**Jabatan**")
tanggal_keluar = st.date_input("**Tanggal Sertifikasi Dikeluarkan**")

thresholds = {
    "ph": (6.5, 8.5),
    "Hardness": (0, 200),
    "Solids": (0, 500),
    "Chloramines": (0, 4),
    "Sulfate": (0, 250),
    "Conductivity": (0, 500),
    "Organic_carbon": (0, 10),
    "Trihalomethanes": (0, 80),
    "Turbidity": (0, 5)
}

satuan = {
    "ph": "-",
    "Hardness": "mg/L",
    "Solids": "mg/L",
    "Chloramines": "mg/L",
    "Sulfate": "mg/L",
    "Conductivity": "µS/cm",
    "Organic_carbon": "mg/L",
    "Trihalomethanes": "µg/L",
    "Turbidity": "NTU"
}


st.divider()

button_place = st.empty()

if button_place.button("Buat Laporan"):
    if (
        not nomor_pengujian or 
        not nama_pelanggan or 
        not alamat_pelanggan or 
        not tanggal_ambil_sample or
        not lokasi_ambil_sample or
        not tanggal_analisa or
        any(input_value == 0.0 for input_value in input_values) or
        any(not metode for metode in metode_pengujian) or
        not penanggung_jawab or
        not jabatan or
        not tanggal_keluar
    ):
        st.toast("⛔️ Mohon isi semua kolom yang ada.")
    else:
        button_place.empty()
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1, text=f"Laporan sedang dibuat... {percent_complete+1}%")
        time.sleep(1)
        my_bar.empty()
        st.success("Laporan anda berhasil dibuat!")
        
        input_data = np.array(input_values).reshape(1, -1)
        prediction = model.predict(input_data)[0]

        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, txt="LABORATORIUM PENGUJIAN KUALITAS AIR", ln=1, align="C")
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 2, txt="LEMBAGA SERTIFIKASI KAMBOJA UTARA", ln=1, align="C")
        
        pdf.ln(3)
        
        pdf.set_font("Arial", "", 9)
        pdf.cell(200, 4, txt="Jl. Letjend Suprapto No.27 10640 Daerah Khusus Ibukota Jakarta", ln=1, align="C")
        
        pdf.set_font("Arial", "", 9)
        pdf.cell(200, 4, txt="Telp.(+62)2518329101, (+62)876290123 ,Fax. 5030100", ln=1, align="C")
        
        pdf.set_font("Arial", "", 9)
        pdf.cell(200, 4 , txt="Website: www.sertifikasikambut.go.id, Email: sertifikasikambut@gmail.com", ln=1, align="C")
        
        pdf.set_font("Arial", "", 12)
        
        try:
            pdf.image("Asset/logo_kanan.png", x=170, y=12, w=28)
        except FileNotFoundError:
            st.error("File logo.png tidak ditemukan. Pastikan file logo berada di direktori yang sama dengan script ini.")
            st.stop()
        
        try:
            pdf.image("Asset/logo_kiri.png", x=10, y=13, w=38)
        except FileNotFoundError:
            st.error("File logo_kiri.png tidak ditemukan. Pastikan file logo berada di direktori yang sama dengan script ini.")
            st.stop()
            

        try:
            pdf.image("Asset/qr_code.png", x=5, y=258   , w=35)
        except FileNotFoundError:
            st.error("File logo_kiri.png tidak ditemukan. Pastikan file logo berada di direktori yang sama dengan script ini.")
            st.stop()
            
            
        pdf.ln(13)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 4, txt="Laporan Hasil Pengujian Kualitas Air", ln=1, align="L")
        
        pdf.ln(3)
        
        pdf.set_font("Arial", "", 9)
        pdf.cell(80, 5, "Nomor Pengujian", 0, 0, 'L')
        pdf.set_font("Arial", "", 9)
        pdf.cell(120, 5, f": {nomor_pengujian}", 0, 1, 'L')
        
        pdf.set_font("Arial", "", 9)
        pdf.cell(80, 5, "Nama Pelanggan", 0, 0, 'L')
        pdf.set_font("Arial", "", 9)
        pdf.cell(120, 5, f": {nama_pelanggan}", 0, 1, 'L')

        pdf.set_font("Arial", "", 9)
        pdf.cell(80, 5, "Alamat Pelanggan", 0, 0, 'L')
        pdf.set_font("Arial", "", 9)
        pdf.cell(120, 5, f": {alamat_pelanggan}", 0, 1, 'L')

        pdf.set_font("Arial", "", 9)
        pdf.cell(80, 5, "Tanggal Ambil Sample", 0, 0, 'L')
        pdf.set_font("Arial", "", 9)
        pdf.cell(120, 5, f": {tanggal_ambil_sample.strftime('%Y-%m-%d')}", 0, 1, 'L')

        pdf.set_font("Arial", "", 9)
        pdf.cell(80, 5, "Lokasi Ambil Sample", 0, 0, 'L')
        pdf.set_font("Arial", "", 9)
        pdf.cell(120, 5, f": {lokasi_ambil_sample}", 0, 1, 'L')

        pdf.set_font("Arial", "", 9)
        pdf.cell(80, 5, "Tanggal Analisa", 0, 0, 'L')
        pdf.set_font("Arial", "", 9)
        pdf.cell(120, 5, f": {tanggal_analisa.strftime('%Y-%m-%d')}", 0, 1, 'L')
        
        
        pdf.ln(6)

        pdf.set_line_width(0.5)
        pdf.line(10, 42, 200, 42)
        
        pdf.set_line_width(0.3)
        pdf.set_font("Arial", "B", 9)
        pdf.cell(10, 10, "No", 1, 0, 'C')
        pdf.cell(50, 10, "Kandungan", 1, 0, 'C')
        pdf.cell(25, 10, "Satuan", 1, 0, 'C')
        pdf.cell(30, 10, "Hasil Uji", 1, 0, 'C')
        pdf.cell(30, 10, "Ambang Batas", 1, 0, 'C')
        pdf.cell(45, 10, "Metode Pengujian", 1, 1, 'C')


        for i, feature in enumerate(features):
            pdf.set_font("Arial", "", 10)
            pdf.cell(10, 10, str(i + 1), 1, 0, 'C')
            pdf.cell(50, 10, feature, 1, 0, 'C')
            pdf.cell(25, 10, satuan[feature], 1, 0, 'C')
            pdf.set_font("Arial", "B", 10)
            pdf.cell(30, 10, str(input_values[i]), 1, 0, 'C')
            pdf.set_font("Arial", "", 10)
            pdf.cell(30, 10, str(thresholds[feature][1]), 1, 0, 'C')
            pdf.cell(45, 10, metode_pengujian[i], 1, 1, 'C')
        
        pdf.ln(2)
        
        conclusion = "MEMENUHI SYARAT" if prediction == 1 else "TIDAK MEMENUHI SYARAT"
        pdf.set_font("Arial", "B", 9)
        pdf.cell(200, 8, f"Kesimpulan : Sample Air yang diuji {conclusion} untuk Digunakan.", ln=1, align="L")
        pdf.cell(200, 4, f"Keterangan : ", ln=1, align="L")
        pdf.set_font("Arial", "", 8)
        pdf.multi_cell(200, 5, f"           *) Klasifikasi kategori kelayakan hasil uji ditentukan secara otomatis dengan dukungan kecerdasan buatan.\n           **) Ambang batas yang dituliskan merujuk pada Permenkes No.492/MENKES/PER/IV/2010.\n            ***) Ini adalah project fiktif. Segala data, informasi, dan juga hak cipta yang digunakan tidak 100% benar.", align="L")
        
        
        pdf.set_xy(pdf.w - 100, pdf.h - 60)
        pdf.set_font("Arial", "", 9 )
        tanggal_rilis = "Bogor, " + datetime.now().strftime("%d %B %Y")
        pdf.cell(90, 5, tanggal_rilis, ln=1, align="C")

        pdf.set_x(pdf.w - 100)
        pdf.set_font("Arial", "B", 9)
        pdf.cell(90, 4, txt="Laboratorium Pengujiar Kualitas Air", ln=1, align="C")

        pdf.set_x(pdf.w - 100)
        pdf.set_font("Arial", "B", 9)
        pdf.cell(90, 4, txt="Lembaga Sertifikasi Kamboja Utara", ln=1, align="C")

        pdf.ln(18)
        
        pdf.set_x(pdf.w - 100)
        pdf.set_font("Arial", "BU", 9)
        pdf.cell(90, 4, penanggung_jawab, ln=1, align="C")

        pdf.set_x(pdf.w - 100)
        pdf.set_font("Arial", "", 9)
        pdf.cell(90, 4, jabatan, ln=1, align="C")
        
        
        pdf.output("sertifikat_kualitas_air.pdf")
        st.markdown("")
        with open("sertifikat_kualitas_air.pdf", "rb") as f:
            st.download_button("Download Laporan", f, "sertifikat_kualitas_air.pdf")
