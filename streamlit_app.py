
import streamlit as st

st.set_page_config(
    page_title="Deskap Laundry Aseli",
    page_icon="🧺",
    layout="centered"
)

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
        radial-gradient(circle at 90% 30%, #c8f0f2 0 11px, transparent 12px),
        radial-gradient(circle at 20% 85%, #ffffff 0 9px, transparent 10px),
        linear-gradient(135deg, #eaf8fb, #d9f0f3);
}

.block-container {
    max-width: 700px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(135deg, #126477, #20a6a2);
    padding: 28px 22px;
    border-radius: 22px;
    color: white;
    text-align: center;
    box-shadow: 0 8px 20px #12647730;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 30px;
    margin-bottom: 8px;
}

.hero p {
    color: #e3ffff;
    margin: 0;
}

.stTextInput input {
    border-radius: 12px;
    background-color: white;
    border: 1px solid #9bcfd2;
}

.stButton button {
    border-radius: 12px;
    min-height: 48px;
    font-weight: bold;
    border: 1px solid #168b91;
}

.stButton button:hover {
    border-color: #126477;
    color: #126477;
}

h2, h3 {
    color: #126477;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="hero">
    <h1>🧺 Deskap Laundry Aseli</h1>
    <p>✨ Bersih, Wangi, dan Praktis ✨</p>
    <p>Solusi Perhitungan Laundry Kiloan</p>
</div>
""", unsafe_allow_html=True)

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
        st.write(f"**Tarif per kg:** Rp {tarif:,.0f}".replace(",", "."))
        st.write(f"**Jumlah digit genap:** {digit_genap}")
        st.write(f"**Persen diskon:** {persen_diskon}%")
        st.write(f"**Biaya normal:** Rp {biaya_normal:,.0f}".replace(",", "."))
        st.write(f"**Potongan:** Rp {potongan:,.0f}".replace(",", "."))

        st.success(
            f"🧺 Total Bayar: Rp {total_bayar:,.0f}".replace(",", ".")
        )

st.divider()
st.caption("🫧 Deskap Laundry Aseli | Fresh Laundry, Fresh Day!")
