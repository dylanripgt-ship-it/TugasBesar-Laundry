import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Laundry Mas Haqi", layout="wide")

st.title("Laundry Mas Haqi")
st.markdown("### Sistem Pencatatan Order & Kasir")

if "orders" not in st.session_state:
    st.session_state.orders = []

LAYANAN = {
    "Cuci Kering Lipat (Kg)": 7000,
    "Cuci Setrika (Kg)": 10000,
    "Setrika Saja (Kg)": 6000,
    "Bed Cover (Satuan)": 25000,
}

with st.form("form_order", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        nama_pelanggan = st.text_input("Nama Pelanggan")
        no_hp = st.text_input("No. HP / WhatsApp")
    with col2:
        layanan = st.selectbox("Jenis Layanan", list(LAYANAN.keys()))
        jumlah = st.number_input("Jumlah (Kg / Pcs)", min_value=0.5, step=0.5, value=1.0)
    with col3:
        status_bayar = st.selectbox("Status Pembayaran", ["Belum Lunas", "Lunas"])
        status_laundry = st.selectbox("Status Cucian", ["Diterima", "Proses Cuci", "Siap Diambil", "Selesai"])

    submitted = st.form_submit_button("Simpan Order")
    if submitted:
        if nama_pelanggan.strip():
            total = int(LAYANAN[layanan] * jumlah)
            st.session_state.orders.append({
                "Kode": f"LMH-{len(st.session_state.orders) + 1:04d}",
                "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Pelanggan": nama_pelanggan.strip(),
                "No. HP": no_hp.strip(),
                "Layanan": layanan,
                "Jumlah": jumlah,
                "Total (Rp)": total,
                "Pembayaran": status_bayar,
                "Status": status_laundry,
            })
            st.success(f"Order untuk **{nama_pelanggan}** berhasil ditambahkan (Total: Rp {total:,}).")
        else:
            st.error("Nama pelanggan wajib diisi.")

st.divider()
st.subheader("Daftar Order")

if st.session_state.orders:
    df = pd.DataFrame(st.session_state.orders)
    st.dataframe(df, use_container_width=True)

    pendapatan = df[df["Pembayaran"] == "Lunas"]["Total (Rp)"].sum()
    st.metric("Total Pendapatan (Lunas)", f"Rp {pendapatan:,}")
else:
    st.info("Belum ada data order masuk.")
