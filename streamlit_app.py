
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
.stApp [data-testid="stWidgetLabel"] p {
    color: #173b45 !important;
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
    color: #ffffff !important;
    border-radius: 12px;
    min-height: 48px;
    font-weight: bold;
    border: none;
}

.stButton button:hover {
    background-color: #126477 !important;
    color: #ffffff !important;
}

.stSuccess {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# JUDUL
st.title("🧺 Deskap Laundry Aseli")


# LAYANAN KAMI
st.markdown("""
<div style="background-color:#fff8df; border:2px solid #e5c66b; border-radius:16px; padding:20px; margin-bottom:20px;">
<h3 style="color:#174b58 !important;">✨ Layanan Kami:</h3>
<p style="color:#263b46 !important;">🧺 Terima cuci baju biar <b>wangy</b></p>
<p style="color:#263b46 !important;">🫧 Cuci muka biar <b>segar</b></p>
<p style="color:#263b46 !important;">🧠 Cuci otak biar <b>sadar</b></p>
<p style="color:#263b46 !important;">😹 Cuci dosa? <i>Next time kita kasih paham</i></p>
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
    st.button(
        "🔄 Reset",
        use_container_width=True,
        on_click=reset_form
    )


# PERHITUNGAN
if hitung:

    if len(nim) != 10 or not nim.isdigit():
        st.error("NIM harus terdiri dari tepat 10 digit angka.")

    elif not berat.isdigit() or int(berat) <= 0:
        st.error("Berat cucian harus berupa bilangan bulat positif.")

    else:
        berat_kg = int(berat)

        tarif = 5000 + (int(nim[-1]) * 500)

        digit_genap = sum(
            int(angka) % 2 == 0 for angka in nim
        )

        persen_diskon = digit_genap * 1

        biaya_normal = berat_kg * tarif
        potongan = biaya_normal * persen_diskon / 100
        total_bayar = biaya_normal - potongan

        st.divider()
        st.subheader("📋 Rincian Perhitungan")

        st.write(f"**NIM:** {nim}")
        st.write(f"**Berat cucian:** {berat_kg} kg")
        st.write(
            f"**Tarif per kg:** Rp {tarif:,.0f}".replace(",", ".")
        )
        st.write(f"**Jumlah digit genap:** {digit_genap}")
        st.write(f"**Persen diskon:** {persen_diskon}%")
        st.write(
            f"**Biaya normal:** Rp {biaya_normal:,.0f}".replace(",", ".")
        )
        st.write(
            f"**Potongan:** Rp {potongan:,.0f}".replace(",", ".")
        )

        st.success(
            f"🧺 Total Bayar: Rp {total_bayar:,.0f}".replace(",", ".")
        )


# FOOTER
st.divider()
st.markdown("""
<div style="text-align:center; color:#126477; font-weight:bold; padding:15px;">
🧺 Deskap Laundry Aseli
</div>
""", unsafe_allow_html=True)
