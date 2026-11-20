import time
import streamlit as st

st.set_page_config(page_title="Laundry Mas Haqi", page_icon="🧺", layout="centered")

DURASI_CUCI = 2.5  # lama animasi mesin cuci berputar (detik)

# ===== Animasi mesin cuci (SVG + CSS) =====
ANIMASI_CSS = """
<style>
.mesin { transform-origin: 50px 50px; animation: getar 0.3s linear infinite; }
.drum { transform-origin: 50px 60px; animation: putar 1.8s linear infinite; }
.air { animation: ombak 1.2s ease-in-out infinite alternate; }
.gelembung { animation: naik 2s ease-in infinite; }
.g2 { animation-delay: 0.7s; }
.g3 { animation-delay: 1.3s; }
@keyframes putar { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes getar {
    0%   { transform: translate(0, 0); }
    25%  { transform: translate(0.8px, -0.5px); }
    50%  { transform: translate(0, 0.5px); }
    75%  { transform: translate(-0.8px, -0.3px); }
    100% { transform: translate(0, 0); }
}
@keyframes ombak { from { transform: translateY(0); } to { transform: translateY(-4px); } }
@keyframes naik { from { transform: translateY(0); opacity: 0.9; } to { transform: translateY(-22px); opacity: 0; } }
@keyframes kedip { 0%, 100% { opacity: 0.2; } 50% { opacity: 1; } }
</style>
"""

MESIN_SVG = "".join(baris.strip() for baris in """
<svg viewBox="0 0 100 100" width="80" height="80" xmlns="http://www.w3.org/2000/svg">
<defs><clipPath id="kaca"><circle cx="50" cy="60" r="24"/></clipPath></defs>
<g class="mesin">
<rect x="10" y="5" width="80" height="90" rx="10" fill="#E2E8F0" stroke="#64748B" stroke-width="2"/>
<rect x="10" y="5" width="80" height="22" rx="10" fill="#CBD5E1"/>
<circle cx="24" cy="16" r="4" fill="#3B82F6"/>
<circle cx="36" cy="16" r="3" fill="#94A3B8"/>
<rect x="60" y="11" width="22" height="10" rx="3" fill="#1E293B"/>
<circle cx="50" cy="60" r="28" fill="#94A3B8" stroke="#475569" stroke-width="3"/>
<circle cx="50" cy="60" r="24" fill="#DBEAFE"/>
<g clip-path="url(#kaca)">
<rect class="air" x="20" y="62" width="60" height="30" fill="#60A5FA" opacity="0.6"/>
<g class="drum">
<circle cx="40" cy="55" r="7" fill="#F472B6"/>
<circle cx="62" cy="64" r="7" fill="#FACC15"/>
<rect x="46" y="68" width="12" height="9" rx="2" fill="#34D399"/>
</g>
<circle class="gelembung g1" cx="38" cy="74" r="2.5" fill="#FFFFFF" opacity="0.8"/>
<circle class="gelembung g2" cx="52" cy="76" r="2" fill="#FFFFFF" opacity="0.8"/>
<circle class="gelembung g3" cx="62" cy="74" r="3" fill="#FFFFFF" opacity="0.8"/>
</g>
<path d="M32 50 A20 20 0 0 1 46 40" stroke="#FFFFFF" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.7"/>
</g>
</svg>
""".splitlines())

# Versi besar untuk animasi saat proses menghitung
MESIN_SVG_BESAR = MESIN_SVG.replace('width="80" height="80"', 'width="150" height="150"')

st.markdown(ANIMASI_CSS, unsafe_allow_html=True)

# ===== Adegan latar: awan, burung camar, pulau, matahari/bulan =====
AWAN_SVG = ("<svg viewBox='0 0 120 50' xmlns='http://www.w3.org/2000/svg'>"
            "<ellipse cx='35' cy='32' rx='28' ry='14'/>"
            "<ellipse cx='62' cy='24' rx='26' ry='18'/>"
            "<ellipse cx='88' cy='32' rx='26' ry='14'/>"
            "<rect x='35' y='30' width='55' height='16' rx='8'/></svg>")

CAMAR_SVG = ("<svg class='sayap' viewBox='0 0 50 24' xmlns='http://www.w3.org/2000/svg'>"
             "<path d='M2 18 Q14 2 25 14 Q36 2 48 18' fill='none' stroke='currentColor' "
             "stroke-width='3' stroke-linecap='round'/>"
             "<circle cx='25' cy='14' r='2.5' fill='currentColor'/></svg>")

PULAU_SVG = ("<svg viewBox='0 0 240 140' xmlns='http://www.w3.org/2000/svg'>"
             # gundukan pasir
             "<path d='M0 140 L0 98 Q40 72 92 82 Q142 68 186 94 Q216 106 240 140 Z' fill='#FDE68A'/>"
             "<path d='M0 118 Q60 100 120 108 Q180 100 240 140 L0 140 Z' fill='#FCD34D' opacity='0.6'/>"
             # rumput
             "<path d='M20 92 Q50 78 92 84 Q130 76 160 90 Q120 92 90 94 Q50 94 20 100 Z' fill='#4ADE80'/>"
             # pohon kelapa besar (bergoyang)
             "<g class='palem'>"
             "<path d='M72 86 Q82 52 68 22' stroke='#92400E' stroke-width='6' fill='none' stroke-linecap='round'/>"
             "<path d='M68 22 Q42 4 16 24 Q44 16 68 22 Z' fill='#16A34A'/>"
             "<path d='M68 22 Q94 2 122 20 Q94 16 68 22 Z' fill='#22C55E'/>"
             "<path d='M68 22 Q50 30 34 52 Q58 40 68 22 Z' fill='#15803D'/>"
             "<path d='M68 22 Q88 30 104 50 Q80 40 68 22 Z' fill='#16A34A'/>"
             "<circle cx='66' cy='26' r='3.5' fill='#78350F'/>"
             "<circle cx='73' cy='27' r='3.5' fill='#78350F'/>"
             "</g>"
             # pohon kecil
             "<g class='palem p2'>"
             "<path d='M140 90 Q146 70 138 54' stroke='#92400E' stroke-width='4' fill='none' stroke-linecap='round'/>"
             "<path d='M138 54 Q120 42 104 56 Q122 52 138 54 Z' fill='#22C55E'/>"
             "<path d='M138 54 Q156 42 172 56 Q154 52 138 54 Z' fill='#16A34A'/>"
             "</g>"
             # batu kecil
             "<ellipse cx='190' cy='112' rx='10' ry='6' fill='#94A3B8'/>"
             "</svg>")

MATAHARI_SVG = ("<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'>"
                "<defs><radialGradient id='glowMatahari'>"
                "<stop offset='0%' stop-color='#FEF08A' stop-opacity='0.9'/>"
                "<stop offset='100%' stop-color='#FDE047' stop-opacity='0'/>"
                "</radialGradient></defs>"
                "<circle class='cahaya' cx='50' cy='50' r='48' fill='url(#glowMatahari)'/>"
                "<g class='sinar' stroke='#FBBF24' stroke-width='4' stroke-linecap='round'>"
                "<line x1='50' y1='6' x2='50' y2='16'/><line x1='50' y1='84' x2='50' y2='94'/>"
                "<line x1='6' y1='50' x2='16' y2='50'/><line x1='84' y1='50' x2='94' y2='50'/>"
                "<line x1='19' y1='19' x2='26' y2='26'/><line x1='74' y1='74' x2='81' y2='81'/>"
                "<line x1='81' y1='19' x2='74' y2='26'/><line x1='26' y1='74' x2='19' y2='81'/>"
                "</g>"
                "<circle cx='50' cy='50' r='20' fill='#FACC15' stroke='#F59E0B' stroke-width='2'/>"
                "<circle cx='43' cy='43' r='6' fill='#FEF9C3' opacity='0.6'/></svg>")

BULAN_SVG = ("<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'>"
             "<defs><radialGradient id='glowBulan'>"
             "<stop offset='0%' stop-color='#E2E8F0' stop-opacity='0.45'/>"
             "<stop offset='100%' stop-color='#E2E8F0' stop-opacity='0'/>"
             "</radialGradient>"
             "<mask id='potongBulan'><rect width='100' height='100' fill='#fff'/>"
             "<circle cx='66' cy='42' r='25' fill='#000'/></mask></defs>"
             "<circle class='cahaya' cx='50' cy='50' r='48' fill='url(#glowBulan)'/>"
             "<circle cx='48' cy='52' r='28' fill='#F1F5F9' mask='url(#potongBulan)'/>"
             "<circle cx='36' cy='58' r='3.5' fill='#CBD5E1' opacity='0.8'/>"
             "<circle cx='42' cy='70' r='2.5' fill='#CBD5E1' opacity='0.8'/></svg>")

# Bintang kecil (hanya mode gelap): (kiri%, atas%, ukuran px, delay detik)
BINTANG = [(6, 8, 4, 0), (14, 20, 3, 0.6), (30, 6, 3, 1.1), (42, 16, 4, 0.3),
           (55, 5, 3, 1.5), (66, 22, 3, 0.9), (76, 10, 4, 0.2), (90, 28, 3, 1.3),
           (24, 30, 3, 0.7), (48, 32, 2, 1.8)]


def bintang_html():
    return "".join(
        f"<div class='bintang' style='left:{x}%;top:{y}%;width:{u}px;height:{u}px;"
        f"animation-delay:-{d}s'></div>" for x, y, u, d in BINTANG)


def awan(kelas):
    return f"<div class='awan {kelas}'>{AWAN_SVG}</div>"


def camar(top, lebar, durasi, delay, arah):
    svg = CAMAR_SVG.replace("<svg ", f"<svg style='width:{lebar}px;animation-delay:-{delay % 1}s' ")
    return (f"<div class='camar {arah}' style='top:{top}%;animation-duration:{durasi}s;"
            f"animation-delay:-{delay}s'><div class='naik' style='animation-delay:-{delay % 3}s'>"
            f"{svg}</div></div>")


def adegan_html(gelap: bool):
    """Adegan latar: matahari (terang) atau bulan + bintang (gelap)."""
    benda = (f"<div class='benda bulan'>{BULAN_SVG}</div>" + bintang_html()
             if gelap else f"<div class='benda matahari'>{MATAHARI_SVG}</div>")
    return "<div class='adegan'>" + benda + "".join([
        awan("a1"), awan("a2"), awan("a3"), awan("a4"),
        camar(8, 40, 22, 3, "kanan"),
        camar(16, 32, 28, 14, "kanan"),
        camar(26, 36, 25, 8, "kiri"),
        camar(12, 26, 34, 20, "kiri"),
        camar(32, 30, 30, 1, "kanan"),
        f"<div class='pulau'>{PULAU_SVG}</div>",
    ]) + "</div>"


# ===== Palet warna tema terang & gelap =====
TEMA = {
    "terang": {
        "LATAR": "linear-gradient(180deg, #E0F2FE 0%, #7DD3FC 55%, #0EA5E9 100%)",
        "KARTU_BG": "rgba(255,255,255,0.92)",
        "OMBAK1": "%23FFFFFF", "OMBAK2": "%230369A1",
        "AWAN": "#FFFFFF", "AWAN_OP": "0.9", "CAMAR": "#334155",
        "BG": "#FFFFFF", "TEKS": "#1F2937", "SUB": "#475569",
        "BORDER_KARTU": "#93C5FD", "INPUT_BG": "#FFFFFF", "INPUT_BORDER": "#CBD5E1",
        "BTN_PRIMER": "#1E40AF", "BTN_SEK_BG": "#FFFFFF", "BTN_SEK_TEKS": "#1E40AF",
        "BTN_SEK_BORDER": "#93C5FD", "JUDUL_RINCIAN": "#1E3A8A", "GARIS": "#BFDBFE",
        "BIRU": "#DBEAFE", "UNGU": "#EDE9FE", "HIJAU": "#DCFCE7",
        "ORANYE": "#FFEDD5", "TOTAL": "#BBF7D0", "BORDER_KOTAK": "rgba(0,0,0,0.06)",
    },
    "gelap": {
        "LATAR": "linear-gradient(180deg, #0B1B3A 0%, #0C3B66 55%, #0E5A7E 100%)",
        "KARTU_BG": "rgba(15,23,42,0.88)",
        "OMBAK1": "%2338BDF8", "OMBAK2": "%23020617",
        "AWAN": "#94A3B8", "AWAN_OP": "0.35", "CAMAR": "#E2E8F0",
        "BG": "#0F172A", "TEKS": "#F1F5F9", "SUB": "#CBD5E1",
        "BORDER_KARTU": "#3B82F6", "INPUT_BG": "#1E293B", "INPUT_BORDER": "#475569",
        "BTN_PRIMER": "#2563EB", "BTN_SEK_BG": "#1E293B", "BTN_SEK_TEKS": "#93C5FD",
        "BTN_SEK_BORDER": "#3B82F6", "JUDUL_RINCIAN": "#93C5FD", "GARIS": "#334155",
        "BIRU": "#1E3A8A", "UNGU": "#4C1D95", "HIJAU": "#14532D",
        "ORANYE": "#7C2D12", "TOTAL": "#166534", "BORDER_KOTAK": "rgba(255,255,255,0.12)",
    },
}

CSS = """
<style>
/* Latar laut */
.stApp {
    background: %%LATAR%% !important;
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: transparent !important;
}
.block-container { position: relative; z-index: 1; }

/* Ombak bergerak di bagian bawah layar */
.stApp::before, .stApp::after {
    content: "";
    position: fixed;
    left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 0;
    background-repeat: repeat-x;
    background-position: 0 bottom;
}
.stApp::before {
    height: 120px;
    background-size: 1200px 120px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M0,60 C150,100 350,0 600,50 C850,100 1050,10 1200,60 L1200,120 L0,120 Z' fill='%%OMBAK1%%' fill-opacity='0.4'/%3E%3C/svg%3E");
    animation: ombakGeser1 14s linear infinite;
}
.stApp::after {
    height: 90px;
    background-size: 900px 90px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M0,60 C150,100 350,0 600,50 C850,100 1050,10 1200,60 L1200,120 L0,120 Z' fill='%%OMBAK2%%' fill-opacity='0.4'/%3E%3C/svg%3E");
    animation: ombakGeser2 9s linear infinite;
}
@keyframes ombakGeser1 { from { background-position-x: 0; } to { background-position-x: 1200px; } }
@keyframes ombakGeser2 { from { background-position-x: 0; } to { background-position-x: -900px; } }

/* Adegan latar: awan, camar, pulau (di belakang kartu) */
.adegan {
    position: fixed; inset: 0; overflow: hidden;
    pointer-events: none; z-index: -1;
}
.awan { position: absolute; left: 0; animation: awanGeser linear infinite; }
.awan svg { fill: %%AWAN%%; opacity: %%AWAN_OP%%; }
.awan.a1 { top: 5%;  animation-duration: 70s;  animation-delay: -10s; }
.awan.a1 svg { width: 190px; }
.awan.a2 { top: 15%; animation-duration: 95s;  animation-delay: -50s; }
.awan.a2 svg { width: 140px; }
.awan.a3 { top: 24%; animation-duration: 120s; animation-delay: -80s; }
.awan.a3 svg { width: 220px; }
.awan.a4 { top: 9%;  animation-duration: 80s;  animation-delay: -30s; }
.awan.a4 svg { width: 120px; }
@keyframes awanGeser {
    from { transform: translateX(-300px); }
    to   { transform: translateX(calc(100vw + 300px)); }
}

.camar { position: absolute; left: 0; color: %%CAMAR%%; animation-timing-function: linear; animation-iteration-count: infinite; }
.camar.kanan { animation-name: terbangKanan; }
.camar.kiri  { animation-name: terbangKiri; }
.camar .naik { animation: naikTurun 3s ease-in-out infinite alternate; }
.camar .sayap { display: block; transform-origin: 50% 60%; animation: kepak 0.7s ease-in-out infinite alternate; }
@keyframes terbangKanan { from { transform: translateX(-100px); } to { transform: translateX(calc(100vw + 100px)); } }
@keyframes terbangKiri  { from { transform: translateX(calc(100vw + 100px)); } to { transform: translateX(-100px); } }
@keyframes naikTurun { from { transform: translateY(-10px); } to { transform: translateY(12px); } }
@keyframes kepak { from { transform: scaleY(1); } to { transform: scaleY(0.3); } }

/* Matahari & bulan */
.benda {
    position: absolute; top: 7%; right: clamp(24px, 9vw, 140px);
    width: clamp(80px, 10vw, 130px);
}
.benda svg { display: block; width: 100%; height: auto; overflow: visible; }
.benda .cahaya { transform-origin: 50px 50px; animation: denyut 3s ease-in-out infinite alternate; }
.matahari .sinar { transform-origin: 50px 50px; animation: putarSinar 30s linear infinite; }
.bulan { animation: melayang 6s ease-in-out infinite alternate; }
@keyframes putarSinar { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes denyut { from { transform: scale(0.92); opacity: 0.8; } to { transform: scale(1.08); opacity: 1; } }
@keyframes melayang { from { transform: translateY(-4px); } to { transform: translateY(6px); } }
.bintang {
    position: absolute; border-radius: 50%; background: #F8FAFC;
    box-shadow: 0 0 6px 2px rgba(248,250,252,0.7);
    animation: kedip 2.2s ease-in-out infinite;
}

/* Pulau di pojok kiri bawah */
.pulau {
    position: absolute; left: -8px; bottom: -4px;
    width: clamp(160px, 22vw, 270px);
}
.pulau svg { display: block; width: 100%; height: auto; }
.pulau .palem { transform-origin: 72px 86px; animation: goyangPalem 4s ease-in-out infinite alternate; }
.pulau .palem.p2 { transform-origin: 140px 90px; animation-duration: 5s; animation-delay: -1.5s; }
@keyframes goyangPalem {
    from { transform: rotate(-2.5deg); }
    to   { transform: rotate(2.5deg); }
}

.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label, .stApp span,
.stApp [data-testid="stCaptionContainer"] { color: %%TEKS%% !important; }

/* Kartu utama */
[data-testid="stVerticalBlockBorderWrapper"] {
    border: 2px solid %%BORDER_KARTU%% !important;
    border-radius: 16px !important;
    background-color: %%KARTU_BG%%;
    padding: 8px 12px;
}

/* Kotak isian */
.stApp input { background-color: %%INPUT_BG%% !important; color: %%TEKS%% !important; }
.stApp [data-baseweb="input"], .stApp [data-baseweb="base-input"] {
    background-color: %%INPUT_BG%% !important;
}
.stApp [data-baseweb="input"] { border: 1px solid %%INPUT_BORDER%%; border-radius: 8px; }
.stApp [data-testid="stNumberInputStepUp"],
.stApp [data-testid="stNumberInputStepDown"] {
    background-color: %%INPUT_BG%% !important; color: %%TEKS%% !important;
}

/* Tombol */
.stApp button[kind="primary"], .stApp button[data-testid="stBaseButton-primary"] {
    background-color: %%BTN_PRIMER%% !important; color: #FFFFFF !important;
    border: 1px solid %%BTN_PRIMER%% !important; border-radius: 8px;
}
.stApp button[kind="primary"] *, .stApp button[data-testid="stBaseButton-primary"] * {
    color: #FFFFFF !important;
}
.stApp button[kind="secondary"], .stApp button[data-testid="stBaseButton-secondary"] {
    background-color: %%BTN_SEK_BG%% !important; color: %%BTN_SEK_TEKS%% !important;
    border: 1px solid %%BTN_SEK_BORDER%% !important; border-radius: 8px;
}
.stApp button[kind="secondary"] *, .stApp button[data-testid="stBaseButton-secondary"] * {
    color: %%BTN_SEK_TEKS%% !important;
}

/* Efek timbul (pop up) pada tombol Hitung & Reset */
.stApp button[kind="primary"], .stApp button[data-testid="stBaseButton-primary"],
.stApp button[kind="secondary"], .stApp button[data-testid="stBaseButton-secondary"] {
    font-weight: 700;
    box-shadow: 0 4px 0 rgba(0,0,0,0.25), 0 8px 14px rgba(0,0,0,0.18);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stApp button[kind="primary"]:hover, .stApp button[data-testid="stBaseButton-primary"]:hover,
.stApp button[kind="secondary"]:hover, .stApp button[data-testid="stBaseButton-secondary"]:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 7px 0 rgba(0,0,0,0.25), 0 14px 22px rgba(0,0,0,0.22);
}
.stApp button[kind="primary"]:active, .stApp button[data-testid="stBaseButton-primary"]:active,
.stApp button[kind="secondary"]:active, .stApp button[data-testid="stBaseButton-secondary"]:active {
    transform: translateY(3px) scale(0.97);
    box-shadow: 0 1px 0 rgba(0,0,0,0.25), 0 2px 5px rgba(0,0,0,0.2);
}

/* Panel rincian (kanan) */
.judul-rincian { font-size: 1.15rem; font-weight: 700; color: %%JUDUL_RINCIAN%%; margin-bottom: 10px; }
.panel { border-left: 2px solid %%GARIS%%; padding-left: 18px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
.kotak {
    border-radius: 12px; padding: 10px 14px;
    display: flex; align-items: center; gap: 10px;
    border: 1px solid %%BORDER_KOTAK%%;
}
.kotak .ikon { font-size: 1.5rem; line-height: 1; }
.kotak .ikon-persen {
    background: #7C3AED; color: #FFF !important; font-weight: 700;
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; font-size: 0.95rem;
}
.kotak .judul { font-size: 0.75rem; color: %%SUB%% !important; }
.kotak .nilai { font-size: 1.15rem; font-weight: 700; color: %%TEKS%% !important; }
.biru   { background-color: %%BIRU%%; }
.ungu   { background-color: %%UNGU%%; }
.hijau  { background-color: %%HIJAU%%; }
.oranye { background-color: %%ORANYE%%; }
.total {
    background-color: %%TOTAL%%; border-radius: 12px; padding: 12px 16px;
    display: flex; align-items: center; justify-content: space-between;
    border: 1px solid %%BORDER_KOTAK%%;
}
.total .kiri { display: flex; align-items: center; gap: 10px;
               font-size: 1.15rem; font-weight: 700; color: %%TEKS%% !important; }
.total .kiri span { color: %%TEKS%% !important; }
.total .kanan { font-size: 1.25rem; font-weight: 700; color: %%TEKS%% !important; }

/* Tampilan saat mesin cuci berputar (proses menghitung) */
.proses {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; min-height: 250px; text-align: center;
}
.proses .teks-proses {
    margin-top: 6px; font-size: 1.1rem; font-weight: 700; color: %%JUDUL_RINCIAN%% !important;
}
.proses .titik { animation: kedip 1s infinite; color: %%JUDUL_RINCIAN%% !important; }
.proses .t2 { animation-delay: 0.25s; }
.proses .t3 { animation-delay: 0.5s; }

/* Bar loading di bawah mesin cuci */
.proses .loading {
    width: 70%; max-width: 260px; height: 12px; margin-top: 14px;
    border-radius: 999px; overflow: hidden;
    background: %%GARIS%%; border: 1px solid %%BORDER_KOTAK%%;
}
.proses .loading-isi {
    height: 100%; width: 0; border-radius: 999px;
    background-color: %%BTN_PRIMER%%;
    background-image: linear-gradient(45deg, rgba(255,255,255,0.3) 25%, transparent 25%,
        transparent 50%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0.3) 75%, transparent 75%);
    background-size: 24px 24px;
    animation: isiLoading linear forwards, garisJalan 0.8s linear infinite;
}
@keyframes isiLoading { from { width: 0; } to { width: 100%; } }
@keyframes garisJalan { from { background-position: 0 0; } to { background-position: 24px 0; } }
</style>
"""


def terapkan_tema(gelap: bool):
    """Menyuntikkan CSS dan adegan latar sesuai tema yang dipilih."""
    css = CSS
    for kunci, nilai in TEMA["gelap" if gelap else "terang"].items():
        css = css.replace(f"%%{kunci}%%", nilai)
    st.markdown(css + "\n" + adegan_html(gelap), unsafe_allow_html=True)


def rupiah(angka: int) -> str:
    """Format angka ke Rupiah, contoh: 80750 -> Rp 80.750"""
    return "Rp " + f"{angka:,}".replace(",", ".")


def panel_proses():
    """HTML mesin cuci besar yang sedang berputar + bar loading."""
    return f"""
    <div class="panel proses">
      {MESIN_SVG_BESAR}
      <div class="teks-proses">Sedang mencuci<span class="titik">.</span><span class="titik t2">.</span><span class="titik t3">.</span></div>
      <div class="loading"><div class="loading-isi" style="animation-duration:{DURASI_CUCI}s, 0.8s"></div></div>
    </div>
    """


def panel_rincian(h):
    """Membuat HTML panel Rincian Perhitungan (kanan)."""
    if h:
        tarif, persen = rupiah(h["tarif"]), f"{h['persen']} %"
        normal, potongan = rupiah(h["normal"]), rupiah(h["potongan"])
        total = rupiah(h["total"])
    else:
        tarif = persen = normal = potongan = total = "-"

    return f"""
    <div class="panel">
      <div class="judul-rincian">Rincian Perhitungan</div>
      <div class="grid">
        <div class="kotak biru">
          <div class="ikon">🏷️</div>
          <div><div class="judul">Tarif per kg</div><div class="nilai">{tarif}</div></div>
        </div>
        <div class="kotak ungu">
          <div class="ikon-persen">%</div>
          <div><div class="judul">Diskon</div><div class="nilai">{persen}</div></div>
        </div>
        <div class="kotak hijau">
          <div class="ikon">🧾</div>
          <div><div class="judul">Biaya normal</div><div class="nilai">{normal}</div></div>
        </div>
        <div class="kotak oranye">
          <div class="ikon">✂️</div>
          <div><div class="judul">Potongan</div><div class="nilai">{potongan}</div></div>
        </div>
      </div>
      <div class="total">
        <div class="kiri"><span>👛</span><span>Total Bayar</span></div>
        <div class="kanan">{total}</div>
      </div>
    </div>
    """


def reset_form():
    """Mengosongkan kotak isian dan hasil."""
    st.session_state["nim"] = ""
    st.session_state["berat"] = None
    st.session_state["hasil"] = None
    st.session_state["hasil_siap"] = None
    st.session_state["animasi"] = False
    st.session_state["error"] = None


# Inisialisasi session state
st.session_state.setdefault("nim", "")
st.session_state.setdefault("hasil", None)
st.session_state.setdefault("hasil_siap", None)
st.session_state.setdefault("animasi", False)
st.session_state.setdefault("error", None)
st.session_state.setdefault("gelap", False)

# Terapkan tema sesuai pilihan saklar
terapkan_tema(st.session_state["gelap"])


def hitung():
    nim = st.session_state["nim"].strip()
    berat = st.session_state.get("berat")
    st.session_state["hasil"] = None
    st.session_state["hasil_siap"] = None
    st.session_state["animasi"] = False
    st.session_state["error"] = None

    # Validasi NIM: tepat 10 digit angka
    if not (len(nim) == 10 and nim.isdigit()):
        st.session_state["error"] = "NIM tidak valid! NIM harus terdiri dari tepat 10 digit angka."
        return

    # Validasi berat: bilangan bulat > 0
    if berat is None:
        st.session_state["error"] = "Berat cucian tidak valid! Masukkan bilangan bulat."
        return
    if berat <= 0:
        st.session_state["error"] = "Berat cucian harus lebih dari 0!"
        return

    # Perhitungan
    digit_terakhir = int(nim[-1])
    tarif = 5000 + digit_terakhir * 500
    digit_genap = sum(1 for d in nim if int(d) % 2 == 0)  # 0,2,4,6,8
    persen_diskon = digit_genap * 1
    biaya_normal = berat * tarif
    potongan = persen_diskon * biaya_normal // 100
    total = biaya_normal - potongan

    # Hasil disimpan dulu; baru ditampilkan setelah animasi selesai
    st.session_state["hasil_siap"] = {
        "tarif": tarif,
        "persen": persen_diskon,
        "normal": biaya_normal,
        "potongan": potongan,
        "total": total,
    }
    st.session_state["animasi"] = True


# ===== Tampilan GUI (landscape) =====
_, kolom_tema = st.columns([3, 1])
with kolom_tema:
    st.toggle("🌙 Mode Gelap", key="gelap")

with st.container(border=True):
    kolom_logo, kolom_judul = st.columns([1, 5], vertical_alignment="center")
    with kolom_logo:
        st.markdown(MESIN_SVG, unsafe_allow_html=True)
    with kolom_judul:
        st.markdown("## Laundry Mas Haqi")
        st.caption("Hitung cepat biaya laundry kiloan")

    kiri, kanan = st.columns([1, 1.5], gap="medium")

    with kiri:
        st.text_input("NIM (10 digit)", key="nim", max_chars=30)
        st.number_input("Berat Cucian (kg)", key="berat", value=None, step=1)
        b1, b2 = st.columns(2)
        b1.button("🧮 Hitung", on_click=hitung, type="primary",
                  help="Tekan untuk menjumlahkan")
        b2.button("🔄 Reset", on_click=reset_form,
                  help="Tekan untuk mengulang")

    with kanan:
        slot = st.empty()
        if st.session_state["animasi"]:
            # Tampilkan mesin cuci berputar, lalu munculkan hasilnya
            slot.markdown(panel_proses(), unsafe_allow_html=True)
            time.sleep(DURASI_CUCI)
            st.session_state["hasil"] = st.session_state["hasil_siap"]
            st.session_state["animasi"] = False
        slot.markdown(panel_rincian(st.session_state["hasil"]), unsafe_allow_html=True)

if st.session_state["error"]:
    st.error(st.session_state["error"])
