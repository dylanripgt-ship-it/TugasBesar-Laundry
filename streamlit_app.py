import random
import time

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
    st.toast("Cucian dibilas bersih ✨")


if "nim" not in st.session_state:
    st.session_state.nim = ""

if "berat" not in st.session_state:
    st.session_state.berat = ""


# GELEMBUNG BUSA ACAK (BACKGROUND)
random.seed(7)
gelembung = "".join(
    f'<span style="left:{random.randint(2, 96)}%;'
    f'width:{u}px;height:{u}px;'
    f'animation-duration:{random.randint(7, 15)}s;'
    f'animation-delay:{random.uniform(0, 10):.1f}s;"></span>'
    for u in [random.randint(8, 30) for _ in range(20)]
)


# DESAIN TAMPILAN + ANIMASI
st.markdown(f"""
<style>
/* BACKGROUND AIR BERGERAK */
.stApp {{
    background: linear-gradient(-45deg, #eaf8fb, #bcebef, #d9f0f3, #ffffff);
    background-size: 400% 400%;
    animation: air 14s ease infinite;
}}

@keyframes air {{
    0%   {{ background-position: 0% 50%; }}
    50%  {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* GELEMBUNG BUSA NAIK */
.bubbles {{
    position: fixed;
    inset: 0;
    pointer-events: none;
    overflow: hidden;
    z-index: 0;
}}

.bubbles span {{
    position: absolute;
    bottom: -40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.6);
    border: 2px solid rgba(139, 203, 208, 0.9);
    animation: naik linear infinite;
}}

@keyframes naik {{
    0%   {{ transform: translateY(0) translateX(0); opacity: 0; }}
    10%  {{ opacity: 1; }}
    50%  {{ transform: translateY(-55vh) translateX(12px); }}
    100% {{ transform: translateY(-110vh) translateX(-8px); opacity: 0; }}
}}

/* KONTEN DI ATAS GELEMBUNG */
.block-container {{
    position: relative;
    z-index: 1;
    max-width: 700px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}}

/* JUDUL */
.stApp h1 {{
    color: #126477 !important;
    font-weight: 800;
}}

/* TEKS UMUM */
.stApp h2,
.stApp h3,
.stApp label,
.stApp p,
.stApp li,
.stApp [data-testid="stWidgetLabel"] p {{
    color: #173b45 !important;
}}

/* KOTAK LAYANAN */
.layanan {{
    background-color: #fff8df;
    border: 2px solid #e5c66b;
    border-radius: 16px;
    padding: 14px 18px;
    color: #263b46;
    line-height: 1.8;
    margin-bottom: 16px;
    font-weight: 400;
}}

.layanan .judul {{
    font-weight: 700;
}}

/* ================= MESIN CUCI ================= */
.area-mesin {{
    position: relative;
    width: 170px;
    margin: 10px auto 0 auto;
}}

.busa-atas {{
    position: absolute;
    top: -22px;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 20px;
}}

.busa-atas span {{
    display: inline-block;
    animation: melayang 2s ease-in-out infinite;
}}

.busa-atas span:nth-child(2) {{ animation-delay: 0.5s; }}
.busa-atas span:nth-child(3) {{ animation-delay: 1s; }}

@keyframes melayang {{
    0%, 100% {{ transform: translateY(0); opacity: 0.4; }}
    50%      {{ transform: translateY(-10px); opacity: 1; }}
}}

.mesin {{
    width: 170px;
    height: 190px;
    border-radius: 22px;
    background: linear-gradient(#ffffff, #e3f4f6);
    border: 4px solid #126477;
    position: relative;
    box-shadow: 0 8px 18px rgba(18, 100, 119, 0.3);
    animation: getar 0.25s linear infinite;
}}

@keyframes getar {{
    0%   {{ transform: translate(0, 0) rotate(0deg); }}
    25%  {{ transform: translate(-2px, 1px) rotate(-0.8deg); }}
    50%  {{ transform: translate(2px, -1px) rotate(0.8deg); }}
    75%  {{ transform: translate(-1px, -1px) rotate(-0.5deg); }}
    100% {{ transform: translate(0, 0) rotate(0deg); }}
}}

.panel {{
    position: absolute;
    top: 10px;
    left: 14px;
    right: 14px;
    height: 22px;
    border-bottom: 3px solid #bcdfe3;
}}

.panel .knob {{
    position: absolute;
    top: 2px;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #e5c66b;
    border: 2px solid #b8962f;
}}

.panel .knob.k1 {{ left: 2px; }}
.panel .knob.k2 {{ left: 24px; background: #8bcbd0; border-color: #168b91; }}

.panel .lampu {{
    position: absolute;
    right: 2px;
    top: 4px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #3ddc84;
    animation: kedip 0.8s steps(2) infinite;
}}

@keyframes kedip {{
    0%   {{ opacity: 1; }}
    100% {{ opacity: 0.25; }}
}}

/* PINTU / DRUM */
.drum {{
    position: absolute;
    left: 50%;
    bottom: 16px;
    width: 120px;
    height: 120px;
    margin-left: -60px;
    border-radius: 50%;
    border: 6px solid #168b91;
    background: #e6fbff;
    overflow: hidden;
    box-shadow: inset 0 0 12px rgba(18, 100, 119, 0.35);
}}

/* AIR BERGELOMBANG */
.air {{
    position: absolute;
    left: -50%;
    top: 42%;
    width: 200%;
    height: 200%;
    background: rgba(22, 139, 145, 0.5);
    border-radius: 38%;
    animation: ombak 3.5s linear infinite;
}}

@keyframes ombak {{
    to {{ transform: rotate(360deg); }}
}}

/* BAJU BERPUTAR */
.baju {{
    position: absolute;
    inset: 0;
    animation: putar 1.6s linear infinite;
}}

.baju span {{
    position: absolute;
    font-size: 26px;
}}

.baju .b1 {{ top: 6px; left: 46px; }}
.baju .b2 {{ bottom: 12px; left: 10px; }}
.baju .b3 {{ bottom: 12px; right: 10px; }}

@keyframes putar {{
    to {{ transform: rotate(360deg); }}
}}

/* GELEMBUNG DALAM DRUM */
.gel {{
    position: absolute;
    bottom: 8px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.85);
    animation: naikdrum 1.8s ease-in infinite;
}}

.gel.g1 {{ left: 26px; width: 8px; height: 8px; }}
.gel.g2 {{ left: 58px; width: 12px; height: 12px; animation-delay: 0.6s; }}
.gel.g3 {{ left: 88px; width: 7px; height: 7px; animation-delay: 1.1s; }}

@keyframes naikdrum {{
    0%   {{ transform: translateY(0); opacity: 0; }}
    20%  {{ opacity: 1; }}
    100% {{ transform: translateY(-80px); opacity: 0; }}
}}

/* KACA PANTULAN */
.drum::after {{
    content: "";
    position: absolute;
    top: 10px;
    left: 14px;
    width: 30px;
    height: 14px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.55);
    transform: rotate(-30deg);
}}

/* STATUS TEKS */
.stApp .sedang-cuci {{
    text-align: center;
    color: #126477 !important;
    font-weight: bold;
    font-size: 17px;
    margin: 12px 0 4px 0;
}}

/* PROGRESS BAR */
.stProgress div[role="progressbar"] > div,
.stProgress > div > div > div > div {{
    background-color: #168b91 !important;
}}

/* KOTAK TOTAL BAYAR */
.total {{
    background: #0f5f66;
    color: #ffffff !important;
    padding: 18px;
    border-radius: 14px;
    font-weight: bold;
    font-size: 20px;
    text-align: center;
    margin: 12px 0;
    animation: muncul 0.6s ease;
}}

@keyframes muncul {{
    0%   {{ transform: scale(0.9); opacity: 0; }}
    100% {{ transform: scale(1); opacity: 1; }}
}}

/* INPUT */
.stTextInput input {{
    background-color: #ffffff !important;
    color: #173b45 !important;
    border: 2px solid #8bcbd0 !important;
    border-radius: 12px;
    min-height: 45px;
}}

/* TOMBOL */
.stButton button {{
    background-color: #168b91 !important;
    border-radius: 12px;
    min-height: 48px;
    font-weight: bold;
    border: none;
    transition: transform 0.15s;
}}

.stButton button:active {{
    transform: scale(0.95);
}}

.stButton button p,
.stButton button span {{
    color: #ffffff !important;
}}

.stButton button:hover {{
    background-color: #126477 !important;
}}
</style>

<div class="bubbles">{gelembung}</div>
""", unsafe_allow_html=True)


# HEADER
st.title("🧺 Deskap Laundry Aseli")


# LAYANAN KAMI
st.markdown("""
<div class="layanan">
<span class="judul">✨ Layanan Kami:</span><br>
• Terima cuci baju biar wangy<br>
• Cuci muka biar segar<br>
• Cuci otak biar sadar<br>
• Cuci dosa? Next time kita kasi paham 😹
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


MESIN_HTML = """
<div class="area-mesin">
  <div class="busa-atas"><span>🫧</span><span>🫧</span><span>🫧</span></div>
  <div class="mesin">
    <div class="panel">
      <div class="knob k1"></div>
      <div class="knob k2"></div>
      <div class="lampu"></div>
    </div>
    <div class="drum">
      <div class="air"></div>
      <div class="baju"><span class="b1">👕</span><span class="b2">🧦</span><span class="b3">👖</span></div>
      <div class="gel g1"></div>
      <div class="gel g2"></div>
      <div class="gel g3"></div>
    </div>
  </div>
</div>
"""

LANGKAH = [
    "🫧 Merendam cucian...",
    "🧼 Mengucek dengan deterjen...",
    "💦 Membilas sampai bersih...",
    "🌀 Memeras air...",
    "✨ Hampir selesai...",
]

# PROSES PERHITUNGAN
if hitung:
    nim_v = nim.strip()
    berat_v = berat.strip()

    if len(nim_v) != 10 or not nim_v.isdecimal():
        st.error("NIM harus terdiri dari tepat 10 digit angka.")

    elif not berat_v.isdecimal() or int(berat_v) <= 0:
        st.error("Berat cucian harus berupa bilangan bulat positif.")

    else:
        # ANIMASI MESIN CUCI SAAT MENGHITUNG
        tempat_mesin = st.empty()
        tempat_status = st.empty()
        tempat_bar = st.empty()

        tempat_mesin.markdown(MESIN_HTML, unsafe_allow_html=True)
        bar = tempat_bar.progress(0)

        for i, langkah in enumerate(LANGKAH):
            tempat_status.markdown(
                f'<div class="sedang-cuci">{langkah}</div>',
                unsafe_allow_html=True
            )
            time.sleep(0.7)
            bar.progress(int((i + 1) / len(LANGKAH) * 100))

        tempat_mesin.empty()
        tempat_status.empty()
        tempat_bar.empty()
        st.toast("Cucian selesai! ✨")

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

        st.markdown(
            f'<div class="total">🧺 Total Bayar: {rupiah(total_bayar)}</div>',
            unsafe_allow_html=True
        )


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
