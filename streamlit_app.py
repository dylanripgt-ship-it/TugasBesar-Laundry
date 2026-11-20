import streamlit as st

st.set_page_config(
    page_title="Deskap Laundry Aseli",
    page_icon="🧺",
    layout="centered"
)


# RESET FORM
def reset_form():
    st.session_state.nim = ""
    st.session_state.berat = ""


if "nim" not in st.session_state:
    st.session_state.nim = ""

if "berat" not in st.session_state:
    st.session_state.berat = ""


# DESAIN TAMPILAN
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 15%, #ffffff 0 7px, transparent 8px),
        radial-gradient(circle at 90% 30%, #bcebef 0 11px, transparent 12px),
        radial-gradient(circle at 20% 85%, #ffffff 0 9px, transparent 10px),
        linear-gradient(135deg, #eaf8fb, #d9f0f3);
}

.block-container {
    max-width: 700px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.stApp h1 {
    color: #126477 !important;
    font-weight: 800;
}

.stApp h2,
.stApp h3,
.stApp label,
.stApp p,
.stApp li,
.stApp [data-testid="stWidgetLabel"] p {
    color: #173b45 !important;
}

.layanan {
    background-color: #fff8df;
    border: 2px solid #e5c66b;
    border-radius: 16px;
    padding: 14px 18px;
    color: #263b46;
    line-height: 1.8;
    margin-bottom: 16px;
}

.stTextInput input {
    background-color: #ffffff !important;
    color: #173b45 !important;
    border: 2px solid #8bcbd0 !important;
    border-radius: 12px;
    min-height: 45px;
}

.stButton button {
    background-color: #168b91 !important;
    border-radius: 12px;
    min-height: 48px;
    font-weight: bold;
    border: none;
}

.stButton button p,
.stButton button span {
    color: #ffffff !important;
}

.stButton button:hover {
    background-color: #126477 !important;
}
</style>
""", unsafe_allow_html=True)


# HEADER
st.title("🧺 Deskap Laundry Aseli")


# LAYANAN KAMI
st.markdown("""
<div class="layanan">
✨ <b>Layanan Kami:</b><br>
• Terima cuci baju biar <b>wangy</b><br>
• Cuci muka biar <b>segar</b><br>
• Cuci otak biar <b>sadar</b>
</div>
""", unsafe_allow_html=True)

# SLOGAN
st.markdown("""
<div style="
    background-color: #ffffff;
    color: #126477;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    padding: 12px;
    border: 2px solid #8bcbd0;
    border-radius: 12px;
    margin-bottom: 20px;
">
    🫧 Fresh Laundry, Fresh Day! 🧺
</div>
""", unsafe_allow_html=True)


# FORMULIR
st.subheader("🫧 Formulir Laundry")

nim = st.text_input("NIM (10 digit)", key="nim")
berat = st.text_input("Berat Cucian (kg)", key="berat")

col1, col2 = st.columns(2)

with col1:
    hitung = st.button("🧮 Hitung", use_container_width=True)

with col2:
    st.button("🔄 Reset", use_container_width=True, on_click=reset_form)


def rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")


# PROSES PERHITUNGAN
if hitung:
    nim_v = nim.strip()
    berat_v = berat.strip()

    if len(nim_v) != 10 or not nim_v.isdecimal():
        st.error("NIM harus terdiri dari tepat 10 digit angka.")

    elif not berat_v.isdecimal() or int(berat_v) <= 0:
        st.error("Berat cucian harus berupa bilangan bulat positif.")

    else:
        berat_kg = int(berat_v)

        tarif = 5000 + int(nim_v[-1]) * 500
        digit_genap = sum(int(d) % 2 == 0 for d in nim_v)
        persen_diskon = digit_genap * 1

        biaya_normal = berat_kg * tarif
        potongan = biaya_normal * persen_diskon // 100
        total_bayar = biaya_normal - potongan

        st.divider()
        st.subheader("📋 Rincian Perhitungan")

        st.write(f"**NIM:** {nim_v}")
        st.write(f"**Berat cucian:** {berat_kg} kg")
        st.write(f"**Tarif per kg:** {rupiah(tarif)}")
        st.write(f"**Jumlah digit genap:** {digit_genap}")
        st.write(f"**Persen diskon:** {persen_diskon}%")
        st.write(f"**Biaya normal:** {rupiah(biaya_normal)}")
        st.write(f"**Potongan:** {rupiah(potongan)}")

        st.success(f"🧺 Total Bayar: {rupiah(total_bayar)}")


# FOOTER
st.divider()

st.markdown("""
<div style="
    text-align:center;
    color:#126477;
    font-weight:bold;
    padding:15px;
    font-size:14px;
">
    🫧 Deskap Laundry Aseli 🧺<br>
    Terima kasih sudah mempercayakan cucianmu!
</div>
""", unsafe_allow_html=True)
