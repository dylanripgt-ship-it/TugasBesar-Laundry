
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

st.title("🧺 Deskap Laundry Aseli")
st.write("Aplikasi Perhitungan Biaya Laundry")
st.divider()

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
            f"Total Bayar: Rp {total_bayar:,.0f}".replace(",", ".")
        )
