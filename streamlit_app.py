import random
import time

import streamlit as st

st.set_page_config(
    page_title="Deskap Laundry Aseli",
    page_icon="🧺",
    layout="centered"
)


# ================= STATE =================
if "nim" not in st.session_state:
    st.session_state.nim = ""

if "berat" not in st.session_state:
    st.session_state.berat = ""

if "mode" not in st.session_state:
    st.session_state.mode = "siang"

if "hasil" not in st.session_state:
    st.session_state.hasil = ""


def reset_form():
    st.session_state.nim = ""
    st.session_state.berat = ""
    st.session_state.hasil = ""
    st.toast("Cucian dibilas bersih ✨")


def ganti_mode():
    st.session_state.mode = "malam" if st.session_state.mode == "siang" else "siang"


mode = st.session_state.mode


# ================= GENERATOR DEKORASI =================
random.seed(7)

# gelembung busa
gelembung = "".join(
    f'<span style="left:{random.randint(2, 96)}%;'
    f'width:{u}px;height:{u}px;'
    f'animation-duration:{random.randint(7, 15)}s;'
    f'animation-delay:{random.uniform(0, 10):.1f}s;"></span>'
    for u in [random.randint(8, 26) for _ in range(14)]
)

# jemuran
PAKAIAN = ["👕", "🧦", "👖", "👗", "🧣", "👚", "🩳", "🧥", "👕", "🧦"]
jemuran_items = "".join(
    f'<div class="jemur" style="left:{4 + i * 9.2:.1f}%;'
    f'animation-duration:{2 + (i % 3) * 0.5}s;'
    f'animation-delay:-{i * 0.4:.1f}s;">{p}</div>'
    for i, p in enumerate(PAKAIAN)
)

# bintang malam
bintang = "".join(
    f'<span class="bintang{" b" if i % 7 == 0 else ""}" '
    f'style="left:{random.uniform(1, 98):.1f}%;top:{random.uniform(1, 55):.1f}%;'
    f'--u:{random.choice([2, 2, 3, 3, 4])}px;'
    f'animation-duration:{random.uniform(1.8, 4.5):.1f}s;'
    f'animation-delay:-{random.uniform(0, 4):.1f}s;"></span>'
    for i in range(55)
)

# burung siang: (top %, durasi, delay)
BURUNG = [(16, 22, 0), (24, 30, -9), (11, 26, -15), (32, 36, -4), (20, 28, -20)]
burung = "".join(
    f'<div class="burung" style="top:{t}%;animation-duration:{d}s;animation-delay:{w}s;">'
    f'<i style="animation-delay:-{k * 0.7:.1f}s"></i></div>'
    for k, (t, d, w) in enumerate(BURUNG)
)

# pohon: (posisi kiri %, skala)
POHON = [(5, 0.85), (17, 1.15), (31, 0.9), (60, 1.05), (74, 0.8), (90, 1.2)]


def pohon_html():
    return "".join(
        f'<div class="pohon" style="left:{x}%;--u:{u};--w:-{i * 0.37:.2f}s;">'
        '<div class="sway"><div class="tajuk"><i></i><i></i><i></i></div>'
        '<div class="batang"></div></div></div>'
        for i, (x, u) in enumerate(POHON)
    )


def bebek_html():
    return "".join(
        f'<div class="bebek d{n}"><div class="apung"><span>🦆</span></div></div>'
        for n in (1, 2, 3)
    )


def adegan(kls, di_tanah="", efek="", beku=False):
    """Satu pemandangan lengkap (langit-tint, daratan, pohon, sungai, efek)."""
    sungai = (
        '<div class="sungai">'
        '<div class="lapis l-belakang"><div class="ombak o-belakang"></div></div>'
        + ('<div class="es"></div>' if beku else "")
        + bebek_html()
        + ("" if beku else '<div class="lapis l-depan"><div class="ombak o-depan"></div></div>')
        + '</div>'
    )
    return (
        f'<div class="adegan {kls}">'
        '<div class="tint"></div>'
        '<div class="bawah">'
        '<div class="tanah t0"></div><div class="tanah t1"></div><div class="tanah t2"></div>'
        + pohon_html()
        + di_tanah
        + sungai
        + '</div>'
        + f'<div class="efek">{efek}</div>'
        + '</div>'
    )


# ---- MUSIM SEMI: bunga mekar, kelopak, kupu-kupu
BUNGA = ["🌸", "🌼", "🌷", "🌺"]
semi_tanah = "".join(
    f'<span class="bunga m{i % 3 + 1}" '
    f'style="left:{random.uniform(2, 96):.1f}%;bottom:{random.randint(60, 118)}px;'
    f'font-size:{random.randint(15, 22)}px;">{random.choice(BUNGA)}</span>'
    for i in range(16)
)
semi_efek = (
    "".join(
        f'<span class="daun" style="left:{random.uniform(0, 98):.1f}%;font-size:{random.randint(11, 15)}px;'
        f'animation-duration:{random.uniform(9, 14):.1f}s;animation-delay:-{random.uniform(0, 12):.1f}s;">🌸</span>'
        for _ in range(10)
    )
    + '<div class="kupu kp1"><span>🦋</span></div><div class="kupu kp2"><span>🦋</span></div>'
)

# ---- MUSIM HUJAN: hujan deras, awan gelap, petir
hujan_efek = (
    '<div class="awan gelap g1"></div><div class="awan gelap g2"></div><div class="awan gelap g3"></div>'
    '<div class="hujan">'
    + "".join(
        f'<span style="left:{random.uniform(5, 125):.1f}%;height:{random.randint(14, 24)}px;'
        f'animation-duration:{random.uniform(0.5, 0.9):.2f}s;animation-delay:-{random.uniform(0, 1):.2f}s;"></span>'
        for _ in range(42)
    )
    + '</div>'
    '<div class="kilat-layar"></div>'
    '<div class="bolt bl1" style="left:20%"><i></i></div>'
    '<div class="bolt bl2" style="left:56%"><i></i></div>'
    '<div class="bolt bl3" style="left:80%"><i></i></div>'
)

# ---- MUSIM GUGUR: daun menguning dan berjatuhan
DAUN = ["🍂", "🍁", "🍂"]
gugur_tanah = "".join(
    f'<span class="dt p{i % 3 + 1}" style="left:{random.uniform(3, 95):.1f}%;'
    f'bottom:{random.randint(58, 112)}px;">🍂</span>'
    for i in range(14)
)
gugur_efek = "".join(
    f'<span class="daun" style="left:{random.uniform(0, 98):.1f}%;font-size:{random.randint(15, 24)}px;'
    f'animation-duration:{random.uniform(6, 12):.1f}s;animation-delay:-{random.uniform(0, 10):.1f}s;">'
    f'{random.choice(DAUN)}</span>'
    for _ in range(16)
)

# ---- MUSIM SALJU: salju turun, daratan tertutup, sungai membeku
salju_efek = "".join(
    f'<span class="flake" style="left:{random.uniform(0, 98):.1f}%;'
    f'width:{u}px;height:{u}px;animation-duration:{random.uniform(5, 10):.1f}s;'
    f'animation-delay:-{random.uniform(0, 9):.1f}s;"></span>'
    for u in [random.randint(3, 8) for _ in range(38)]
)

ADEGAN = (
    adegan("s-semi", semi_tanah, semi_efek)
    + adegan("s-hujan", "", hujan_efek)
    + adegan("s-gugur", gugur_tanah, gugur_efek)
    + adegan("s-salju", "", salju_efek, beku=True)
)


def dekorasi(mode_aktif):
    if mode_aktif == "malam":
        langit = (
            '<div class="bulan"><i></i><i></i><i></i></div>'
            f'{bintang}'
            '<div class="meteor m1"></div><div class="meteor m2"></div>'
        )
    else:
        langit = (
            '<div class="matahari"></div>'
            '<div class="awan a1"></div><div class="awan a2"></div>'
            '<div class="awan a3"></div><div class="awan a4"></div>'
            f'<div class="kawanan">{burung}</div>'
        )
    return (
        f'<div class="dekor {mode_aktif}">'
        + langit
        + ADEGAN
        + f'<div class="bubbles">{gelembung}</div>'
        + '</div>'
    )


def css_ombak(k, wb, wd):
    return (
        f".{k} .o-belakang{{background-image:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
        f"viewBox='0 0 160 40' preserveAspectRatio='none'%3E%3Cpath d='M0 20Q40 8 80 20T160 20V40H0Z' "
        f"fill='%23{wb}'/%3E%3C/svg%3E\");}}\n"
        f".{k} .o-depan{{background-image:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
        f"viewBox='0 0 100 40' preserveAspectRatio='none'%3E%3Cpath d='M0 20Q25 10 50 20T100 20V40H0Z' "
        f"fill='%23{wd}'/%3E%3C/svg%3E\");}}\n"
    )


CSS_OMBAK = (
    css_ombak("s-semi", "b3e5f0", "7fcfe0")
    + css_ombak("s-hujan", "8fa6b8", "5f7f96")
    + css_ombak("s-gugur", "a6d3d0", "6fb0aa")
    + css_ombak("s-salju", "9fd0e3", "7fb8d6")
)


# ================= CSS UTAMA =================
st.markdown("""
<style>
html, body, .stApp {
    overflow-x: hidden;
}

/* BACKGROUND AIR BERGERAK */
.stApp {
    background: linear-gradient(-45deg, #eaf8fb, #bcebef, #d9f0f3, #ffffff);
    background-size: 400% 400%;
    animation: air 14s ease infinite;
}

@keyframes air {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.block-container {
    position: relative;
    z-index: 1;
    max-width: 700px;
    padding-top: 2rem;
    padding-bottom: 9rem;
}

/* ============ DEKORASI BACKGROUND ============ */
.dekor {
    position: fixed;
    inset: 0;
    pointer-events: none;
    overflow: hidden;
    z-index: 0;
}

/* ---------- MATAHARI (SIANG) ---------- */
.matahari {
    position: absolute;
    top: 64px;
    right: 24px;
    width: 58px;
    height: 58px;
}

.matahari::before {
    content: "";
    position: absolute;
    inset: -18px;
    border-radius: 50%;
    background: repeating-conic-gradient(
        rgba(255, 214, 60, 0.9) 0 8deg,
        transparent 8deg 24deg
    );
    animation: putar 14s linear infinite;
}

.matahari::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: radial-gradient(circle, #fffbd0, #ffe066 60%, #ffc933);
    box-shadow: 0 0 30px 10px rgba(255, 220, 80, 0.95),
                0 0 80px 30px rgba(255, 210, 60, 0.45);
    animation: denyut 3s ease-in-out infinite alternate;
}

@keyframes denyut {
    from { transform: scale(1); }
    to   { transform: scale(1.08); }
}

/* ---------- AWAN ---------- */
.awan {
    position: absolute;
    left: 0;
    width: 90px;
    height: 28px;
    background: rgba(255, 255, 255, 0.92);
    border-radius: 30px;
    animation: awanlewat linear infinite;
}

.awan::before {
    content: "";
    position: absolute;
    width: 44px;
    height: 44px;
    top: -22px;
    left: 14px;
    border-radius: 50%;
    background: inherit;
}

.awan::after {
    content: "";
    position: absolute;
    width: 34px;
    height: 34px;
    top: -16px;
    left: 44px;
    border-radius: 50%;
    background: inherit;
}

.a1 { top: 130px; --s: 1;   animation-duration: 45s; animation-delay: -10s; }
.a2 { top: 230px; --s: 1.4; animation-duration: 65s; animation-delay: -35s; }
.a3 { top: 330px; --s: 0.8; animation-duration: 55s; animation-delay: -20s; }
.a4 { top: 190px; --s: 1.1; animation-duration: 75s; animation-delay: -55s; }

.awan.gelap { background: rgba(70, 80, 98, 0.95); }
.g1 { top: 70px;  --s: 1.9; animation-duration: 38s; animation-delay: -5s; }
.g2 { top: 130px; --s: 1.5; animation-duration: 50s; animation-delay: -28s; }
.g3 { top: 40px;  --s: 2.2; animation-duration: 62s; animation-delay: -40s; }

@keyframes awanlewat {
    from { transform: translateX(-220px) scale(var(--s)); }
    to   { transform: translateX(calc(100vw + 220px)) scale(var(--s)); }
}

/* ---------- BURUNG TERBANG (SIANG) ---------- */
.kawanan {
    position: absolute;
    inset: 0;
    animation: v-burung 20s linear infinite;
}

@keyframes v-burung {
    0%, 22%   { opacity: 1; }
    26%, 51%  { opacity: 0; }
    55%, 100% { opacity: 1; }
}

.burung {
    position: absolute;
    left: -50px;
    width: 28px;
    height: 12px;
    animation: terbang linear infinite;
}

.burung i {
    position: absolute;
    inset: 0;
    display: block;
    animation: naikturun 1.6s ease-in-out infinite alternate;
}

.burung i::before,
.burung i::after {
    content: "";
    position: absolute;
    top: 2px;
    width: 13px;
    height: 7px;
    border-top: 3px solid #3b4a5a;
    border-radius: 60% 60% 0 0;
}

.burung i::before {
    left: 0;
    transform-origin: 100% 100%;
    animation: kepak-kiri 0.32s ease-in-out infinite alternate;
}

.burung i::after {
    left: 14px;
    transform-origin: 0 100%;
    animation: kepak-kanan 0.32s ease-in-out infinite alternate;
}

@keyframes terbang   { to { transform: translateX(calc(100vw + 100px)); } }
@keyframes naikturun { from { transform: translateY(-8px); } to { transform: translateY(8px); } }
@keyframes kepak-kiri  { from { transform: rotate(-28deg); } to { transform: rotate(22deg); } }
@keyframes kepak-kanan { from { transform: rotate(28deg); } to { transform: rotate(-22deg); } }

/* ---------- BULAN & BINTANG (MALAM) ---------- */
.bulan {
    position: absolute;
    top: 62px;
    right: 26px;
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, #ffffff, #fff6c8 55%, #e9d98f);
    box-shadow: 0 0 28px 10px rgba(255, 246, 190, 0.65),
                0 0 90px 36px rgba(255, 246, 190, 0.28);
    animation: sinar-bulan 5s ease-in-out infinite alternate;
}

.bulan i {
    position: absolute;
    border-radius: 50%;
    background: rgba(190, 170, 110, 0.35);
}

.bulan i:nth-child(1) { left: 14px; top: 16px; width: 16px; height: 16px; }
.bulan i:nth-child(2) { left: 40px; top: 36px; width: 22px; height: 22px; }
.bulan i:nth-child(3) { left: 20px; top: 46px; width: 10px; height: 10px; }

@keyframes sinar-bulan {
    from { box-shadow: 0 0 22px 8px rgba(255, 246, 190, 0.55), 0 0 70px 28px rgba(255, 246, 190, 0.2); }
    to   { box-shadow: 0 0 34px 14px rgba(255, 246, 190, 0.85), 0 0 110px 44px rgba(255, 246, 190, 0.35); }
}

.bintang {
    position: absolute;
    width: var(--u);
    height: var(--u);
    border-radius: 50%;
    background: #ffffff;
    box-shadow: 0 0 6px 2px rgba(255, 255, 255, 0.85);
    animation: kelip ease-in-out infinite alternate;
}

.bintang.b {
    width: 5px;
    height: 5px;
    box-shadow: 0 0 10px 4px rgba(255, 255, 255, 0.95), 0 0 22px 8px rgba(190, 220, 255, 0.5);
}

.bintang.b::before,
.bintang.b::after {
    content: "";
    position: absolute;
    background: linear-gradient(90deg, transparent, #ffffff, transparent);
}

.bintang.b::before { left: -9px; right: -9px; top: 2px; height: 1px; }
.bintang.b::after  { top: -9px; bottom: -9px; left: 2px; width: 1px;
                     background: linear-gradient(transparent, #ffffff, transparent); }

@keyframes kelip {
    from { opacity: 0.35; transform: scale(0.8); }
    to   { opacity: 1;    transform: scale(1.25); }
}

.meteor {
    position: absolute;
    width: 110px;
    height: 2px;
    border-radius: 2px;
    background: linear-gradient(90deg, transparent, #ffffff);
    opacity: 0;
    animation: meteor 9s linear infinite;
}

.meteor.m1 { left: 12%; top: 8%; }
.meteor.m2 { left: 45%; top: 18%; animation-duration: 13s; animation-delay: -5s; }

@keyframes meteor {
    0%, 86% { opacity: 0; transform: translate(0, 0) rotate(33deg); }
    88%     { opacity: 1; }
    96%     { opacity: 0; transform: translate(340px, 220px) rotate(33deg); }
    100%    { opacity: 0; transform: translate(340px, 220px) rotate(33deg); }
}

/* ---------- GELEMBUNG BUSA ---------- */
.bubbles {
    position: absolute;
    inset: 0;
}

.bubbles span {
    position: absolute;
    bottom: -40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.45);
    border: 2px solid rgba(139, 203, 208, 0.9);
    animation: naik linear infinite;
}

@keyframes naik {
    0%   { transform: translateY(0) translateX(0); opacity: 0; }
    10%  { opacity: 1; }
    50%  { transform: translateY(-55vh) translateX(12px); }
    100% { transform: translateY(-110vh) translateX(-8px); opacity: 0; }
}

/* ============ SIKLUS MUSIM (20 detik = 4 musim x 5 detik) ============ */
.adegan {
    position: absolute;
    inset: 0;
    opacity: 0;
}

.s-semi  { animation: v1 20s linear infinite; }
.s-hujan { animation: v2 20s linear infinite; }
.s-gugur { animation: v3 20s linear infinite; }
.s-salju { animation: v4 20s linear infinite; }

@keyframes v1 { 0% { opacity: 1; } 23% { opacity: 1; } 25% { opacity: 0; } 98% { opacity: 0; } 100% { opacity: 1; } }
@keyframes v2 { 0% { opacity: 0; } 23% { opacity: 0; } 25% { opacity: 1; } 48% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 0; } }
@keyframes v3 { 0% { opacity: 0; } 48% { opacity: 0; } 50% { opacity: 1; } 73% { opacity: 1; } 75% { opacity: 0; } 100% { opacity: 0; } }
@keyframes v4 { 0% { opacity: 0; } 73% { opacity: 0; } 75% { opacity: 1; } 98% { opacity: 1; } 100% { opacity: 0; } }

/* warna langit per musim */
.tint { position: absolute; inset: 0; }
.s-semi  .tint { background: linear-gradient(rgba(255, 200, 230, 0.18), transparent 70%); }
.s-hujan .tint { background: linear-gradient(rgba(70, 80, 100, 0.62), rgba(90, 100, 120, 0.35)); }
.s-gugur .tint { background: linear-gradient(rgba(255, 170, 90, 0.24), rgba(255, 210, 150, 0.08)); }
.s-salju .tint { background: linear-gradient(rgba(235, 245, 255, 0.55), rgba(255, 255, 255, 0.25)); }

.dekor.malam .s-semi  .tint { background: linear-gradient(rgba(200, 150, 220, 0.1), transparent 70%); }
.dekor.malam .s-hujan .tint { background: linear-gradient(rgba(10, 15, 30, 0.55), rgba(10, 15, 30, 0.35)); }
.dekor.malam .s-gugur .tint { background: linear-gradient(rgba(255, 150, 60, 0.1), transparent 70%); }
.dekor.malam .s-salju .tint { background: linear-gradient(rgba(150, 170, 210, 0.2), transparent 70%); }

.bawah { position: absolute; inset: 0; }
.dekor.malam .bawah { filter: brightness(0.45) saturate(0.85); }

.efek { position: absolute; inset: 0; overflow: hidden; }

/* ============ DARATAN ============ */
.tanah { position: absolute; bottom: 50px; }
.t0 { left: 0; right: 0; height: 46px; }
.t1 { left: -6%; width: 68%; height: 86px; border-radius: 50% 50% 0 0 / 100% 100% 0 0; }
.t2 { right: -10%; width: 66%; height: 74px; border-radius: 50% 50% 0 0 / 100% 100% 0 0; filter: brightness(1.08); }

.s-semi  .tanah { background: linear-gradient(#a5e27f, #6fbf55); }
.s-hujan .tanah { background: linear-gradient(#5f9a69, #3f7a4c); }
.s-gugur .tanah { background: linear-gradient(#d2a44b, #a8772f); }
.s-salju .tanah { background: linear-gradient(#a5e27f, #6fbf55); }

/* salju menutupi daratan */
.s-salju .tanah::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: #ffffff;
    transform-origin: 50% 100%;
    transform: scaleY(0);
    animation: tutup 20s linear infinite;
}

@keyframes tutup {
    0%, 76% { transform: scaleY(0); }
    92%, 100% { transform: scaleY(1); }
}

/* ============ POHON ============ */
.pohon {
    position: absolute;
    bottom: 98px;
    width: 60px;
    height: 112px;
    margin-left: -30px;
    transform: scale(var(--u));
    transform-origin: 50% 100%;
}

.sway {
    position: absolute;
    inset: 0;
    transform-origin: 50% 100%;
    animation: goyang-halus 4.5s ease-in-out infinite alternate;
    animation-delay: var(--w);
}

.batang {
    position: absolute;
    bottom: 0;
    left: 50%;
    margin-left: -5px;
    width: 10px;
    height: 60px;
    border-radius: 3px;
    background: linear-gradient(90deg, #8a5a34, #6b4226);
}

.tajuk { position: absolute; top: 0; left: 0; right: 0; height: 76px; }
.tajuk i { position: absolute; border-radius: 50%; background-color: #7fc15a; }
.tajuk i:nth-child(1) { left: 0;    top: 26px; width: 36px; height: 36px; }
.tajuk i:nth-child(2) { left: 24px; top: 26px; width: 36px; height: 36px; }
.tajuk i:nth-child(3) { left: 11px; top: 2px;  width: 40px; height: 40px; }

@keyframes goyang-halus  { from { transform: rotate(-1.5deg); } to { transform: rotate(1.5deg); } }
@keyframes goyang-kencang { from { transform: rotate(2deg); } to { transform: rotate(14deg); } }
@keyframes gigil { from { transform: translateX(-2px); } to { transform: translateX(2px); } }

/* semi: tunas hijau lalu mekar merah muda */
.s-semi .tajuk i { animation: c-semi 20s linear infinite; }
@keyframes c-semi {
    0%   { background-color: #9fd36b; }
    6%   { background-color: #ffc2da; }
    97%  { background-color: #ffb3d1; }
    100% { background-color: #9fd36b; }
}

/* hujan: angin kencang */
.s-hujan .tajuk i { background-color: #2f7a4a; }
.s-hujan .sway { animation: goyang-kencang 0.9s ease-in-out infinite alternate; animation-delay: var(--w); }
.s-hujan .tajuk { animation: gigil 0.25s linear infinite alternate; }

/* gugur: daun menguning */
.s-gugur .sway { animation-duration: 3s; }
.s-gugur .tajuk i { animation: c-gugur 20s linear infinite; }
@keyframes c-gugur {
    0%, 48% { background-color: #8cc15a; }
    56%     { background-color: #f0c23c; }
    66%     { background-color: #e9822c; }
    75%, 100% { background-color: #d3562a; }
}

/* salju: pohon memutih */
.s-salju .sway { animation-duration: 6s; }
.s-salju .tajuk i { animation: c-salju 20s linear infinite; box-shadow: inset 0 -5px 0 rgba(170, 205, 220, 0.6); }
@keyframes c-salju {
    0%, 74% { background-color: #6faa62; }
    86%, 100% { background-color: #f3fbff; }
}

/* ============ EFEK PARTIKEL ============ */
.daun {
    position: absolute;
    top: 0;
    animation: jatuh linear infinite;
}

@keyframes jatuh {
    0%   { transform: translate(0, -6vh) rotate(0deg); }
    25%  { transform: translate(30px, 26vh) rotate(110deg); }
    50%  { transform: translate(-24px, 52vh) rotate(210deg); }
    75%  { transform: translate(28px, 80vh) rotate(300deg); }
    100% { transform: translate(-10px, 108vh) rotate(380deg); }
}

/* bunga mekar */
.bunga {
    position: absolute;
    transform-origin: 50% 100%;
    transform: scale(0);
}
.bunga.m1 { animation: mekar1 20s linear infinite; }
.bunga.m2 { animation: mekar2 20s linear infinite; }
.bunga.m3 { animation: mekar3 20s linear infinite; }

@keyframes mekar1 { 0% { transform: scale(0); } 3% { transform: scale(1.35); } 6%, 97% { transform: scale(1); } 100% { transform: scale(0); } }
@keyframes mekar2 { 0%, 3% { transform: scale(0); } 6% { transform: scale(1.35); } 9%, 97% { transform: scale(1); } 100% { transform: scale(0); } }
@keyframes mekar3 { 0%, 6% { transform: scale(0); } 9% { transform: scale(1.35); } 12%, 97% { transform: scale(1); } 100% { transform: scale(0); } }

/* kupu-kupu */
.kupu { position: absolute; left: 10%; bottom: 150px; animation: kupu-terbang 14s ease-in-out infinite; }
.kupu.kp2 { left: 60%; bottom: 170px; animation-duration: 18s; animation-delay: -6s; }
.kupu span { display: inline-block; font-size: 20px; animation: kepak-kupu 0.28s ease-in-out infinite alternate; }

@keyframes kupu-terbang {
    0%   { transform: translate(0, 0); }
    20%  { transform: translate(120px, -50px); }
    40%  { transform: translate(40px, -110px); }
    60%  { transform: translate(200px, -70px); }
    80%  { transform: translate(90px, -20px); }
    100% { transform: translate(0, 0); }
}
@keyframes kepak-kupu { from { transform: scaleX(1); } to { transform: scaleX(0.3); } }

/* hujan deras miring tertiup angin */
.hujan span {
    position: absolute;
    top: 0;
    width: 2px;
    background: linear-gradient(rgba(200, 225, 255, 0), rgba(200, 225, 255, 0.95));
    animation: hujan linear infinite;
}

@keyframes hujan {
    from { transform: translate(0, -8vh) rotate(14deg); }
    to   { transform: translate(-27vh, 108vh) rotate(14deg); }
}

/* petir */
.kilat-layar { position: absolute; inset: 0; background: #ffffff; opacity: 0; animation: kilat-layar 20s linear infinite; }

@keyframes kilat-layar {
    0%, 29%   { opacity: 0; }
    29.5%     { opacity: 0.85; }
    30.5%     { opacity: 0.15; }
    31%       { opacity: 0.7; }
    33%       { opacity: 0; }
    38.5%     { opacity: 0; }
    39%       { opacity: 0.8; }
    40.5%     { opacity: 0; }
    44%       { opacity: 0; }
    44.4%     { opacity: 0.9; }
    45%       { opacity: 0.2; }
    45.4%     { opacity: 0.75; }
    47%, 100% { opacity: 0; }
}

.bolt {
    position: absolute;
    top: 0;
    width: 90px;
    height: 58vh;
    opacity: 0;
    filter: drop-shadow(0 0 10px #fffbb0) drop-shadow(0 0 22px #bcd8ff);
}

.bolt i {
    display: block;
    width: 100%;
    height: 100%;
    background: linear-gradient(#ffffff, #fff7a8);
    clip-path: polygon(60% 0, 28% 46%, 50% 46%, 30% 100%, 82% 40%, 56% 40%, 78% 0);
}

.bl1 { animation: sambar1 20s linear infinite; }
.bl2 { animation: sambar2 20s linear infinite; }
.bl3 { animation: sambar3 20s linear infinite; }

@keyframes sambar1 { 0%, 29% { opacity: 0; } 29.5% { opacity: 1; } 30.5% { opacity: 0.2; } 31% { opacity: 1; } 32%, 100% { opacity: 0; } }
@keyframes sambar2 { 0%, 38.5% { opacity: 0; } 39% { opacity: 1; } 40.5%, 100% { opacity: 0; } }
@keyframes sambar3 { 0%, 44% { opacity: 0; } 44.4% { opacity: 1; } 45% { opacity: 0.3; } 45.4% { opacity: 1; } 46.5%, 100% { opacity: 0; } }

/* daun menumpuk di tanah (gugur) */
.dt { position: absolute; font-size: 15px; opacity: 0; }
.dt.p1 { animation: tumpuk1 20s linear infinite; }
.dt.p2 { animation: tumpuk2 20s linear infinite; }
.dt.p3 { animation: tumpuk3 20s linear infinite; }
@keyframes tumpuk1 { 0%, 52% { opacity: 0; } 58%, 100% { opacity: 1; } }
@keyframes tumpuk2 { 0%, 58% { opacity: 0; } 64%, 100% { opacity: 1; } }
@keyframes tumpuk3 { 0%, 64% { opacity: 0; } 70%, 100% { opacity: 1; } }

/* salju turun */
.flake {
    position: absolute;
    top: 0;
    border-radius: 50%;
    background: #ffffff;
    box-shadow: 0 0 4px rgba(255, 255, 255, 0.9);
    animation: salju-jatuh linear infinite;
}

@keyframes salju-jatuh {
    0%   { transform: translate(0, -20px); }
    33%  { transform: translate(18px, 35vh); }
    66%  { transform: translate(-14px, 70vh); }
    100% { transform: translate(8px, 108vh); }
}

/* ============ SUNGAI TENANG ============ */
.sungai {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 80px;
}

.lapis { position: absolute; left: 0; right: 0; }
.l-belakang { bottom: 18px; height: 56px; animation: bob 6s ease-in-out infinite; }
.l-depan    { bottom: -6px; height: 56px; animation: bob 5s ease-in-out infinite reverse; }

@keyframes bob {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-3px); }
}

.ombak { position: absolute; left: 0; top: 0; bottom: 0; background-repeat: repeat-x; }
.o-belakang { width: calc(100% + 160px); background-size: 160px 100%; animation: geser160 16s linear infinite reverse; }
.o-depan    { width: calc(100% + 100px); background-size: 100px 100%; animation: geser100 10s linear infinite; }

.s-hujan .l-belakang, .s-hujan .l-depan { animation-duration: 2.4s; }
.s-hujan .o-belakang { animation-duration: 6s; }
.s-hujan .o-depan    { animation-duration: 4s; }

@keyframes geser160 { to { transform: translateX(-160px); } }
@keyframes geser100 { to { transform: translateX(-100px); } }

/* sungai membeku */
.es {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 54px;
    transform-origin: 0 50%;
    transform: scaleX(0);
    background:
        repeating-linear-gradient(115deg, rgba(255, 255, 255, 0.55) 0 2px, transparent 2px 38px),
        linear-gradient(#f2fbff, #bfe6f3);
    border-top: 3px solid #ffffff;
    animation: beku 20s linear infinite;
}

@keyframes beku {
    0%, 76% { transform: scaleX(0); }
    90%, 100% { transform: scaleX(1); }
}

/* ============ BEBEK BERENANG MENYAMPING ============ */
.bebek { position: absolute; left: -70px; animation: lewat linear infinite; }
.bebek .apung { animation: apung 3s ease-in-out infinite; }
.bebek span { display: inline-block; transform: scaleX(-1); }

.d1 { bottom: 34px; font-size: 32px; animation-duration: 40s; animation-delay: -8s; }
.d2 { bottom: 40px; font-size: 24px; animation-duration: 52s; animation-delay: -30s; }
.d3 { bottom: 30px; font-size: 28px; animation-duration: 46s; animation-delay: -18s; }
.d2 .apung { animation-delay: -1s; animation-duration: 3.8s; }
.d3 .apung { animation-delay: -2s; animation-duration: 2.6s; }

@keyframes lewat { to { transform: translateX(calc(100vw + 140px)); } }
@keyframes apung {
    0%, 100% { transform: translateY(0) rotate(-2deg); }
    50%      { transform: translateY(-4px) rotate(2deg); }
}

/* ============ TEKS ============ */
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
    font-weight: 400;
}

.layanan .judul { font-weight: 700; }

.slogan {
    background-color: #ffffff;
    color: #126477;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    padding: 12px;
    border: 2px solid #8bcbd0;
    border-radius: 12px;
    margin-bottom: 20px;
}

.footer {
    text-align: center;
    color: #126477;
    font-weight: bold;
    padding: 15px;
    font-size: 14px;
    background: rgba(255, 255, 255, 0.85);
    border-radius: 14px;
    margin-top: 20px;
}

/* ============ JEMURAN ============ */
.jemuran {
    position: relative;
    height: 66px;
    margin: 4px 0 14px 0;
}

.tali {
    position: absolute;
    top: 4px;
    left: 0;
    right: 0;
    border-top: 3px solid #8d6e63;
}

.tiang {
    position: absolute;
    top: 0;
    width: 5px;
    height: 62px;
    background: #8d6e63;
    border-radius: 3px;
}

.t-kiri  { left: 0; }
.t-kanan { right: 0; }

.jemur {
    position: absolute;
    top: 3px;
    font-size: 30px;
    transform-origin: top center;
    animation: ayun 2.4s ease-in-out infinite alternate;
}

@keyframes ayun {
    from { transform: rotate(-10deg); }
    to   { transform: rotate(10deg); }
}

/* ============ MESIN CUCI ============ */
.area-mesin {
    position: relative;
    width: 170px;
    margin: 20px auto 0 auto;
}

.busa-atas {
    position: absolute;
    top: -22px;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 20px;
}

.busa-atas span {
    display: inline-block;
    animation: melayang 2s ease-in-out infinite;
}

.busa-atas span:nth-child(2) { animation-delay: 0.5s; }
.busa-atas span:nth-child(3) { animation-delay: 1s; }

@keyframes melayang {
    0%, 100% { transform: translateY(0); opacity: 0.4; }
    50%      { transform: translateY(-10px); opacity: 1; }
}

.mesin {
    width: 170px;
    height: 190px;
    border-radius: 22px;
    background: linear-gradient(#ffffff, #e3f4f6);
    border: 4px solid #126477;
    position: relative;
    box-shadow: 0 8px 18px rgba(18, 100, 119, 0.3);
    animation: getar 0.25s linear infinite;
}

@keyframes getar {
    0%   { transform: translate(0, 0) rotate(0deg); }
    25%  { transform: translate(-2px, 1px) rotate(-0.8deg); }
    50%  { transform: translate(2px, -1px) rotate(0.8deg); }
    75%  { transform: translate(-1px, -1px) rotate(-0.5deg); }
    100% { transform: translate(0, 0) rotate(0deg); }
}

.panel {
    position: absolute;
    top: 10px;
    left: 14px;
    right: 14px;
    height: 22px;
    border-bottom: 3px solid #bcdfe3;
}

.panel .knob {
    position: absolute;
    top: 2px;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #e5c66b;
    border: 2px solid #b8962f;
}

.panel .knob.k1 { left: 2px; }
.panel .knob.k2 { left: 24px; background: #8bcbd0; border-color: #168b91; }

.panel .lampu {
    position: absolute;
    right: 2px;
    top: 4px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #3ddc84;
    animation: kedip 0.8s steps(2) infinite;
}

@keyframes kedip {
    0%   { opacity: 1; }
    100% { opacity: 0.25; }
}

.drum {
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
}

.air {
    position: absolute;
    left: -50%;
    top: 42%;
    width: 200%;
    height: 200%;
    background: rgba(22, 139, 145, 0.5);
    border-radius: 38%;
    animation: putar 3.5s linear infinite;
}

.baju {
    position: absolute;
    inset: 0;
    animation: putar 1.6s linear infinite;
}

.baju span {
    position: absolute;
    font-size: 26px;
}

.baju .b1x { top: 6px; left: 46px; }
.baju .b2x { bottom: 12px; left: 10px; }
.baju .b3x { bottom: 12px; right: 10px; }

@keyframes putar {
    to { transform: rotate(360deg); }
}

.gel {
    position: absolute;
    bottom: 8px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.85);
    animation: naikdrum 1.8s ease-in infinite;
}

.gel.g1 { left: 26px; width: 8px; height: 8px; }
.gel.g2 { left: 58px; width: 12px; height: 12px; animation-delay: 0.6s; }
.gel.g3 { left: 88px; width: 7px; height: 7px; animation-delay: 1.1s; }

@keyframes naikdrum {
    0%   { transform: translateY(0); opacity: 0; }
    20%  { opacity: 1; }
    100% { transform: translateY(-80px); opacity: 0; }
}

.drum::after {
    content: "";
    position: absolute;
    top: 10px;
    left: 14px;
    width: 30px;
    height: 14px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.55);
    transform: rotate(-30deg);
}

.stApp .sedang-cuci {
    text-align: center;
    color: #126477 !important;
    font-weight: bold;
    font-size: 17px;
    margin: 12px 0 4px 0;
}

/* ============ KARTU RINCIAN PERHITUNGAN ============ */
.kartu {
    background:
        radial-gradient(circle at 94% 8%, rgba(139, 203, 208, 0.35) 0 28px, transparent 29px),
        radial-gradient(circle at 5% 92%, rgba(139, 203, 208, 0.3) 0 20px, transparent 21px),
        linear-gradient(#ffffff, #eaf8fb);
    border: 2px solid #8bcbd0;
    border-radius: 18px;
    padding: 0 16px 16px 16px;
    margin: 18px 0;
    box-shadow: 0 8px 20px rgba(18, 100, 119, 0.18);
    overflow: hidden;
    animation: muncul 0.6s cubic-bezier(.34, 1.56, .64, 1);
}

.kartu-judul {
    background: linear-gradient(90deg, #126477, #168b91);
    color: #ffffff;
    font-weight: bold;
    font-size: 18px;
    padding: 12px 16px;
    margin: 0 -16px 8px -16px;
}

.baris {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    padding: 10px 2px;
    border-bottom: 1px dashed #8bcbd0;
    color: #173b45;
    font-size: 15px;
    animation: masuk 0.5s ease both;
}

.baris .val {
    font-weight: 700;
    text-align: right;
}

@keyframes masuk {
    from { opacity: 0; transform: translateX(-18px); }
    to   { opacity: 1; transform: translateX(0); }
}

.total {
    background: linear-gradient(90deg, #0f5f66, #168b91);
    color: #ffffff;
    padding: 16px;
    border-radius: 14px;
    font-weight: bold;
    font-size: 20px;
    text-align: center;
    margin-top: 14px;
}

@keyframes muncul {
    0%   { transform: scale(0.88); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}

.error-box {
    background: #ffe3e3;
    border: 2px solid #e57373;
    color: #8b1a1a;
    padding: 14px 18px;
    border-radius: 14px;
    font-weight: bold;
    margin: 12px 0;
    animation: goyang 0.4s;
}

@keyframes goyang {
    0%, 100% { transform: translateX(0); }
    25%      { transform: translateX(-6px); }
    75%      { transform: translateX(6px); }
}

/* ============ INPUT ============ */
div[data-baseweb="input"],
div[data-baseweb="base-input"] {
    background-color: #ffffff !important;
    border-radius: 12px;
}

.stTextInput input {
    background-color: #ffffff !important;
    color: #173b45 !important;
    -webkit-text-fill-color: #173b45 !important;
    border: 2px solid #8bcbd0 !important;
    border-radius: 12px;
    min-height: 45px;
}

/* ============ TOMBOL DENGAN EFEK POP ============ */
.stButton button {
    background-color: #168b91 !important;
    border-radius: 14px;
    min-height: 48px;
    font-weight: bold;
    border: none;
    box-shadow: 0 4px 0 #0f5f66;
    transition:
        transform 0.18s cubic-bezier(.34, 1.56, .64, 1),
        box-shadow 0.18s,
        background-color 0.2s;
    animation: pop 0.5s cubic-bezier(.34, 1.56, .64, 1);
}

.stButton button:hover {
    background-color: #126477 !important;
    transform: translateY(-3px) scale(1.04);
    box-shadow: 0 7px 0 #0f5f66;
}

.stButton button:active {
    transform: translateY(3px) scale(0.92);
    box-shadow: 0 1px 0 #0f5f66;
}

.stButton button p,
.stButton button span {
    color: #ffffff !important;
}

@keyframes pop {
    0%   { transform: scale(0.8); opacity: 0; }
    60%  { transform: scale(1.08); opacity: 1; }
    100% { transform: scale(1); }
}
</style>
""", unsafe_allow_html=True)

# warna ombak sungai tiap musim
st.markdown(f"<style>{CSS_OMBAK}</style>", unsafe_allow_html=True)

# ================= TEMA MALAM =================
if mode == "malam":
    st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #050a24, #0b1640, #1a1f5c, #0a1030);
    background-size: 400% 400%;
    animation: air 14s ease infinite;
}

.stApp h1 {
    color: #9fe3ff !important;
    text-shadow: 0 0 14px rgba(120, 200, 255, 0.6);
}

.stApp h2,
.stApp h3,
.stApp label,
.stApp p,
.stApp li,
.stApp [data-testid="stWidgetLabel"] p {
    color: #dff3ff !important;
}

.layanan {
    background-color: rgba(20, 30, 70, 0.88);
    border-color: #6b7bd6;
    color: #e8f0ff;
}

.slogan {
    background-color: rgba(15, 25, 60, 0.92);
    color: #bfe9ff;
    border-color: #4f78c9;
}

.footer {
    background: rgba(15, 25, 60, 0.88);
    color: #bfe9ff;
}

div[data-baseweb="input"],
div[data-baseweb="base-input"] {
    background-color: #101a3d !important;
}

.stTextInput input {
    background-color: #101a3d !important;
    color: #e8f4ff !important;
    -webkit-text-fill-color: #e8f4ff !important;
    border-color: #5f8fe0 !important;
}

.stButton button {
    background-color: #3b4fb8 !important;
    box-shadow: 0 4px 0 #26358a;
}

.stButton button:hover {
    background-color: #4a5fd0 !important;
    box-shadow: 0 7px 0 #26358a;
}

.stApp .sedang-cuci { color: #bfe9ff !important; }

.kartu {
    background: linear-gradient(#142050, #0c1438);
    border-color: #5f8fe0;
}

.baris {
    color: #e8f4ff;
    border-bottom-color: #5f8fe0;
}

.bubbles span {
    background: rgba(180, 200, 255, 0.2);
    border-color: rgba(150, 180, 255, 0.6);
}
</style>
""", unsafe_allow_html=True)


# ================= DEKORASI (LANGIT + PEMANDANGAN) =================
st.markdown(dekorasi(mode), unsafe_allow_html=True)


# HEADER
st.title("🧺 Deskap Laundry Aseli")

# TOMBOL MODE MALAM / TERANG
st.button(
    "🌙 Mode Malam" if mode == "siang" else "☀️ Mode Terang",
    use_container_width=True,
    on_click=ganti_mode,
    key="tombol_mode"
)

# JEMURAN
st.markdown(
    '<div class="jemuran">'
    '<div class="tiang t-kiri"></div>'
    '<div class="tiang t-kanan"></div>'
    '<div class="tali"></div>'
    f'{jemuran_items}'
    '</div>',
    unsafe_allow_html=True
)


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
<div class="slogan">
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


def kotak_error(pesan):
    st.markdown(
        f'<div class="error-box">⚠️ {pesan}</div>',
        unsafe_allow_html=True
    )


def baris(ikon, label, nilai, urutan):
    return (
        f'<div class="baris" style="animation-delay:{urutan * 0.08:.2f}s">'
        f'<span>{ikon} {label}</span><span class="val">{nilai}</span>'
        f'</div>'
    )


MESIN_HTML = (
    '<div class="area-mesin">'
    '<div class="busa-atas"><span>🫧</span><span>🫧</span><span>🫧</span></div>'
    '<div class="mesin">'
    '<div class="panel">'
    '<div class="knob k1"></div><div class="knob k2"></div><div class="lampu"></div>'
    '</div>'
    '<div class="drum">'
    '<div class="air"></div>'
    '<div class="baju"><span class="b1x">👕</span><span class="b2x">🧦</span><span class="b3x">👖</span></div>'
    '<div class="gel g1"></div><div class="gel g2"></div><div class="gel g3"></div>'
    '</div>'
    '</div>'
    '</div>'
)

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
        st.session_state.hasil = ""
        kotak_error("NIM harus terdiri dari tepat 10 digit angka.")

    elif not berat_v.isdecimal() or int(berat_v) <= 0:
        st.session_state.hasil = ""
        kotak_error("Berat cucian harus berupa bilangan bulat positif.")

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

        # hasil disimpan supaya tidak hilang saat ganti mode terang/malam
        st.session_state.hasil = (
            '<div class="kartu">'
            '<div class="kartu-judul">📋 Rincian Perhitungan</div>'
            + baris("🆔", "NIM", nim_v, 0)
            + baris("⚖️", "Berat cucian", f"{berat_kg} kg", 1)
            + baris("🏷️", "Tarif per kg", rupiah(tarif), 2)
            + baris("🔢", "Jumlah digit genap", digit_genap, 3)
            + baris("🎁", "Persen diskon", f"{persen_diskon}%", 4)
            + baris("💵", "Biaya normal", rupiah(biaya_normal), 5)
            + baris("✂️", "Potongan", rupiah(potongan), 6)
            + f'<div class="total">🧺 Total Bayar: {rupiah(total_bayar)}</div>'
            + '</div>'
        )

if st.session_state.hasil:
    st.markdown(st.session_state.hasil, unsafe_allow_html=True)


# FOOTER
st.markdown("""
<div class="footer">
    🫧 Deskap Laundry Aseli 🧺<br>
    Terima kasih sudah mempercayakan cucianmu!
</div>
""", unsafe_allow_html=True)
