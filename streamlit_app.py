
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
    color: #173b45;
}

.block-container {
    max-width: 700px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* JUDUL */
.stApp h1 {
    color: #126477 !important;
    font-weight: 800;
}

.stApp h2,
.stApp h3,
.stApp label,
.stApp [data-testid="stWidgetLabel"] p,
.stApp .stMarkdown p {
    color: #173b45 !important;
}

/* KOTAK LAYANAN */
[data-testid="stAlert"] {
    background: linear-gradient(135deg, #d0f1f3, #b5e5e9);
    border: 1px solid #168b91;
    border-radius: 16px;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] li,
[data-testid="stAlert"] strong {
    color: #124b58 !important;
}

/* INPUT */
.stTextInput input {
    background-color: #ffffff !important;
    color: #173b45 !important;
    border: 2px solid #8bcbd0 !important;
    border-radius: 12px;
    min-height: 45px;
}

/* TOMBOL */
.stButton button {
    background-color: #168b91;
    color: #ffffff !important;
    border-radius: 12px;
    min-height: 48px;
    font-weight: bold;
    border: none;
}

.stButton button:hover {
    background-color: #126477;
    color: #ffffff !important;
}

/* HASIL */
.stSuccess {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# HEADER DAN LAYANAN
st.title("🧺 Deskap Laundry Aseli")

st.info("""
✨ **Layanan Kami:**

* Terima cuci baju biar **wangy**
* Cuci muka biar **segar**
* Cuci otak biar **sadar**
* Cuci dosa? *Next time kita kasih paham* 😹
""")

st.caption("🫧 Fresh Laundry, Fresh Day!")


# FORMULIR
st.subheader("🫧 Formulir Laundry")

nim = st.text_input("NIM (10 digit)", key="nim")
berat = st.text_input("Berat Cucian (kg)", key="berat")

col1, col2 = st.columns(2)

with col1:
    hitung = st.button(
        "🧮 Hitung",
        use_container_width=True
    )

with col2:
    st.button(
        "🔄 Reset",
        use_container_width=True,
        on_click=reset_form
    )


# PROSES PERHITUNGAN
if hitung:

    # VALIDASI NIM
    if len(nim) != 10 or not nim.isdigit():
        st.error("NIM harus terdiri dari tepat 10 digit angka.")

    # VALIDASI BERAT
    elif not berat.isdigit() or int(berat) <= 0:
        st.error("Berat cucian harus berupa bilangan bulat positif.")

    else:
        berat_kg = int(berat)

        # MENGHITUNG TARIF
        tarif = 5000 + (int(nim[-1]) * 500)

        # MENGHITUNG DIGIT GENAP
        digit_genap = sum(
            int(angka) % 2 == 0 for angka in nim
        )

        # MENGHITUNG DISKON
        persen_diskon = digit_genap * 1

        # MENGHITUNG BIAYA
        biaya_normal = berat_kg * tarif
        potongan = biaya_normal * persen_diskon / 100
        total_bayar = biaya_normal - potongan

        # MENAMPILKAN HASIL
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
<div style="text-align:center; color:#173b45; padding:15px;">
    🫧 <b>Deskap Laundry Aseli</b><br>
    Terima kasih sudah mempercayakan cucianmu kepada kami!
</div>
""", unsafe_allow_html=True)
