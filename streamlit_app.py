import streamlit as st

st.set_page_config(page_title="Laundry Mas Haqi", page_icon="🧺", layout="centered")

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

st.markdown(ANIMASI_CSS, unsafe_allow_html=True)

# ===== Palet warna tema terang & gelap =====
TEMA = {
    "terang": {
        "LATAR": "linear-gradient(180deg, #E0F2FE 0%, #7DD3FC 55%, #0EA5E9 100%)",
        "KARTU_BG": "rgba(255,255,255,0.92)",
        "OMBAK1": "%23FFFFFF", "OMBAK2": "%230369A1",
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
    background: %%LATAR%%;
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: transparent; }
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
</style>
"""


def terapkan_tema(gelap: bool):
    """Menyuntikkan CSS sesuai tema yang dipilih."""
    css = CSS
    for kunci, nilai in TEMA["gelap" if gelap else "terang"].items():
        css = css.replace(f"%%{kunci}%%", nilai)
    st.markdown(css, unsafe_allow_html=True)


def rupiah(angka: int) -> str:
    """Format angka ke Rupiah, contoh: 80750 -> Rp 80.750"""
    return "Rp " + f"{angka:,}".replace(",", ".")


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
    st.session_state["error"] = None


# Inisialisasi session state
st.session_state.setdefault("nim", "")
st.session_state.setdefault("hasil", None)
st.session_state.setdefault("error", None)
st.session_state.setdefault("gelap", False)

# Terapkan tema sesuai pilihan saklar
terapkan_tema(st.session_state["gelap"])


def hitung():
    nim = st.session_state["nim"].strip()
    berat = st.session_state.get("berat")
    st.session_state["hasil"] = None
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

    st.session_state["hasil"] = {
        "tarif": tarif,
        "persen": persen_diskon,
        "normal": biaya_normal,
        "potongan": potongan,
        "total": total,
    }


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
        st.markdown(panel_rincian(st.session_state["hasil"]), unsafe_allow_html=True)

if st.session_state["error"]:
    st.error(st.session_state["error"])
