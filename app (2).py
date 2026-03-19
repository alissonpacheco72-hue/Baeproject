import streamlit as st
import time
import random
import math
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BAE · Baby Ambient Eco-sensor",
    page_icon="👶",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Inject global CSS (Baby Boo aesthetic) ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Fredoka+One&display=swap');

/* ─ Reset & base ─ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #f0f4ec !important;
    font-family: 'Nunito', sans-serif;
}

[data-testid="stAppViewContainer"] > .main {
    background-color: #f0f4ec !important;
}

[data-testid="stHeader"] { background: transparent !important; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f0f4ec; }
::-webkit-scrollbar-thumb { background: #a8c5b8; border-radius: 10px; }

/* ─ Hero header ─ */
.bae-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
}
.bae-title {
    font-family: 'Fredoka One', cursive;
    font-size: 3.8rem;
    color: #7a1e1e;
    letter-spacing: 2px;
    line-height: 1;
    text-shadow: 3px 3px 0px rgba(122,30,30,0.12);
}
.bae-subtitle {
    font-family: 'Nunito', sans-serif;
    font-size: 0.95rem;
    color: #6b8f7e;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 4px;
}
.bae-eco-badge {
    display: inline-block;
    background: #7a1e1e;
    color: #f0f4ec;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 3px 12px;
    border-radius: 20px;
    margin-top: 10px;
    text-transform: uppercase;
}

/* ─ Status card ─ */
.status-card {
    border-radius: 28px;
    padding: 2rem 2.5rem;
    margin: 1.5rem auto;
    max-width: 480px;
    text-align: center;
    transition: all 0.5s ease;
    position: relative;
    overflow: hidden;
}
.status-card.stable {
    background: #d6ece3;
    border: 3px solid #7ec4a4;
    box-shadow: 0 8px 32px rgba(126,196,164,0.25);
}
.status-card.wet {
    background: #fde8e8;
    border: 3px solid #d88080;
    box-shadow: 0 8px 32px rgba(216,128,128,0.25);
}
.status-label {
    font-family: 'Fredoka One', cursive;
    font-size: 1.6rem;
    margin-top: 0.5rem;
}
.status-card.stable .status-label { color: #1a6b4a; }
.status-card.wet .status-label { color: #8b1a1a; }
.status-desc {
    font-size: 0.92rem;
    font-weight: 600;
    margin-top: 6px;
    opacity: 0.75;
}
.status-card.stable .status-desc { color: #1a6b4a; }
.status-card.wet .status-desc { color: #8b1a1a; }

/* ─ Metrics row ─ */
.metrics-row {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    margin: 1.5rem auto;
    max-width: 520px;
}
.metric-chip {
    background: white;
    border-radius: 18px;
    padding: 1rem 1.5rem;
    text-align: center;
    flex: 1;
    min-width: 120px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    border: 2px solid #e8ede6;
}
.metric-icon { font-size: 1.5rem; margin-bottom: 4px; }
.metric-value {
    font-family: 'Fredoka One', cursive;
    font-size: 1.6rem;
    color: #7a1e1e;
    line-height: 1;
}
.metric-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: #8fa89d;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 3px;
}

/* ─ History table ─ */
.history-box {
    background: white;
    border-radius: 20px;
    padding: 1.5rem;
    margin: 1rem auto;
    max-width: 520px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    border: 2px solid #e8ede6;
}
.history-title {
    font-family: 'Fredoka One', cursive;
    font-size: 1.1rem;
    color: #7a1e1e;
    margin-bottom: 1rem;
}
.history-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f0f4ec;
    font-size: 0.85rem;
    font-weight: 600;
    color: #4a6b5e;
}
.history-row:last-child { border-bottom: none; }
.h-dot {
    width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0;
}
.h-dot.stable { background: #7ec4a4; }
.h-dot.wet { background: #d88080; }
.h-time { color: #aab8b3; font-size: 0.78rem; margin-left: auto; }

/* ─ Info section ─ */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    max-width: 520px;
    margin: 1rem auto;
}
.info-card {
    background: white;
    border-radius: 18px;
    padding: 1.2rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    border: 2px solid #e8ede6;
}
.info-card-title {
    font-family: 'Fredoka One', cursive;
    font-size: 0.95rem;
    color: #7a1e1e;
    margin-bottom: 0.5rem;
}
.info-card p {
    font-size: 0.8rem;
    color: #6b8f7e;
    font-weight: 600;
    line-height: 1.5;
}

/* ─ Slider override ─ */
[data-testid="stSlider"] {
    padding: 0 0.5rem;
}

/* ─ Buttons ─ */
.stButton > button {
    background: #7a1e1e !important;
    color: #f0f4ec !important;
    border: none !important;
    border-radius: 50px !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
    letter-spacing: 1px !important;
    box-shadow: 0 4px 12px rgba(122,30,30,0.25) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #9a2e2e !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(122,30,30,0.35) !important;
}

/* ─ Divider ─ */
.bae-divider {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #a8c5b8, transparent);
    max-width: 300px;
    margin: 1.5rem auto;
}

/* ─ Footer ─ */
.bae-footer {
    text-align: center;
    font-size: 0.75rem;
    color: #a8bdb5;
    font-weight: 600;
    padding: 2rem 1rem;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# ── SVG Babies ────────────────────────────────────────────────────────────────
BABY_HAPPY = """
<svg width="140" height="160" viewBox="0 0 140 160" xmlns="http://www.w3.org/2000/svg">
  <style>
    @keyframes breathe { 0%,100%{transform:scaleY(1)} 50%{transform:scaleY(1.04)} }
    @keyframes blink { 0%,90%,100%{transform:scaleY(1)} 95%{transform:scaleY(0.1)} }
    @keyframes curl { 0%,100%{transform:rotate(0deg)} 50%{transform:rotate(5deg)} }
    .body-g { transform-origin: 70px 100px; animation: breathe 2.8s ease-in-out infinite; }
    .eye-l { transform-origin: 54px 72px; animation: blink 4s ease-in-out infinite; }
    .eye-r { transform-origin: 86px 72px; animation: blink 4s ease-in-out infinite 0.1s; }
    .curl-g { transform-origin: 70px 38px; animation: curl 3s ease-in-out infinite; }
  </style>
  <!-- Oval background (mint) -->
  <ellipse cx="70" cy="82" rx="62" ry="72" fill="#aed9cc" opacity="0.5"/>
  <g class="body-g">
    <!-- Bib -->
    <path d="M50 108 Q70 124 90 108 L92 130 Q70 145 48 130 Z" fill="#f8f5f0" stroke="#7a1e1e" stroke-width="2.2" stroke-linejoin="round"/>
    <circle cx="70" cy="122" r="4" fill="none" stroke="#7a1e1e" stroke-width="1.8"/>
    <!-- Body -->
    <ellipse cx="70" cy="104" rx="26" ry="18" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2.2"/>
    <!-- Ears -->
    <ellipse cx="28" cy="68" rx="8" ry="10" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2.2"/>
    <ellipse cx="112" cy="68" rx="8" ry="10" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2.2"/>
    <!-- Head -->
    <circle cx="70" cy="62" r="38" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2.2"/>
    <!-- Hair curl -->
    <g class="curl-g">
      <path d="M64 30 Q62 22 70 20 Q78 18 78 26 Q78 32 72 32" fill="none" stroke="#7a1e1e" stroke-width="2.5" stroke-linecap="round"/>
    </g>
    <!-- Eyes (happy arcs) -->
    <g class="eye-l">
      <path d="M46 70 Q54 62 62 70" fill="none" stroke="#7a1e1e" stroke-width="2.8" stroke-linecap="round"/>
    </g>
    <g class="eye-r">
      <path d="M78 70 Q86 62 94 70" fill="none" stroke="#7a1e1e" stroke-width="2.8" stroke-linecap="round"/>
    </g>
    <!-- Cheeks -->
    <ellipse cx="46" cy="78" rx="9" ry="6" fill="#f4a0a0" opacity="0.55"/>
    <ellipse cx="94" cy="78" rx="9" ry="6" fill="#f4a0a0" opacity="0.55"/>
    <!-- Smile -->
    <path d="M56 84 Q70 96 84 84" fill="none" stroke="#7a1e1e" stroke-width="2.5" stroke-linecap="round"/>
  </g>
</svg>
"""

BABY_CRY = """
<svg width="140" height="160" viewBox="0 0 140 160" xmlns="http://www.w3.org/2000/svg">
  <style>
    @keyframes cry-shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-3px)} 75%{transform:translateX(3px)} }
    @keyframes tear-fall { 0%{transform:translateY(0);opacity:1} 100%{transform:translateY(22px);opacity:0} }
    @keyframes tear-fall2 { 0%{transform:translateY(0);opacity:1} 100%{transform:translateY(18px);opacity:0} }
    .cry-body { transform-origin:70px 80px; animation: cry-shake 0.55s ease-in-out infinite; }
    .tear-l { animation: tear-fall 1s ease-in infinite; }
    .tear-r { animation: tear-fall2 1s ease-in infinite 0.3s; }
  </style>
  <ellipse cx="70" cy="82" rx="62" ry="72" fill="#f5c5c5" opacity="0.4"/>
  <g class="cry-body">
    <!-- Bib -->
    <path d="M50 108 Q70 124 90 108 L92 130 Q70 145 48 130 Z" fill="#f8f5f0" stroke="#7a1e1e" stroke-width="2.2" stroke-linejoin="round"/>
    <circle cx="70" cy="122" r="4" fill="none" stroke="#7a1e1e" stroke-width="1.8"/>
    <!-- Body -->
    <ellipse cx="70" cy="104" rx="26" ry="18" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2.2"/>
    <!-- Ears -->
    <ellipse cx="28" cy="68" rx="8" ry="10" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2.2"/>
    <ellipse cx="112" cy="68" rx="8" ry="10" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2.2"/>
    <!-- Head -->
    <circle cx="70" cy="62" r="38" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2.2"/>
    <!-- Hair curl -->
    <path d="M64 30 Q62 22 70 20 Q78 18 78 26 Q78 32 72 32" fill="none" stroke="#7a1e1e" stroke-width="2.5" stroke-linecap="round"/>
    <!-- Eyes (sad, eyebrows frown) -->
    <path d="M44 58 Q54 54 62 60" fill="none" stroke="#7a1e1e" stroke-width="2" stroke-linecap="round"/>
    <path d="M78 60 Q86 54 96 58" fill="none" stroke="#7a1e1e" stroke-width="2" stroke-linecap="round"/>
    <!-- Pupils teary -->
    <ellipse cx="54" cy="70" rx="5" ry="6" fill="#7a1e1e"/>
    <ellipse cx="86" cy="70" rx="5" ry="6" fill="#7a1e1e"/>
    <ellipse cx="52" cy="68" rx="1.5" ry="2" fill="white"/>
    <ellipse cx="84" cy="68" rx="1.5" ry="2" fill="white"/>
    <!-- Cheeks red -->
    <ellipse cx="44" cy="80" rx="10" ry="7" fill="#e87070" opacity="0.45"/>
    <ellipse cx="96" cy="80" rx="10" ry="7" fill="#e87070" opacity="0.45"/>
    <!-- Frown mouth -->
    <path d="M56 90 Q70 82 84 90" fill="none" stroke="#7a1e1e" stroke-width="2.5" stroke-linecap="round"/>
    <!-- Tears -->
    <g class="tear-l">
      <path d="M50 76 Q48 82 50 88" fill="none" stroke="#6aaad4" stroke-width="2.5" stroke-linecap="round"/>
    </g>
    <g class="tear-r">
      <path d="M90 76 Q92 82 90 88" fill="none" stroke="#6aaad4" stroke-width="2.5" stroke-linecap="round"/>
    </g>
    <!-- Water drops on diaper area hint -->
    <ellipse cx="62" cy="138" rx="4" ry="5" fill="#6aaad4" opacity="0.45"/>
    <ellipse cx="70" cy="142" rx="3" ry="4" fill="#6aaad4" opacity="0.35"/>
    <ellipse cx="78" cy="138" rx="3.5" ry="4.5" fill="#6aaad4" opacity="0.4"/>
  </g>
</svg>
"""

# ── Thresholds (configurable via sidebar) ────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuración BAE")
    st.caption("Umbrales del nano dispositivo")
    hum_threshold = st.slider("💧 Humedad máxima (%)", 40, 90, 65,
                              help="Por encima de este valor = pañal mojado")
    temp_max = st.slider("🌡️ Temperatura máx (°C)", 32, 40, 36,
                         help="Temperatura alta puede indicar malestar")
    temp_min = st.slider("❄️ Temperatura mín (°C)", 20, 30, 24,
                         help="Temperatura baja puede indicar frío")
    st.markdown("---")
    st.markdown("**Materiales ECO del dispositivo:**")
    st.caption("🌿 PCB biodegradable · Sensor orgánico · Carcasa bambú · Tinta vegetal")
    demo_mode = st.toggle("🎮 Modo demostración", value=True)

# ── State init ────────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()
if "sim_humidity" not in st.session_state:
    st.session_state.sim_humidity = 42.0
if "sim_temp" not in st.session_state:
    st.session_state.sim_temp = 28.5
if "sim_direction" not in st.session_state:
    st.session_state.sim_direction = 1

# ── Sensor reading (demo simulation or manual) ────────────────────────────────
if demo_mode:
    # Smooth sinusoidal simulation
    t = time.time()
    humidity = 45 + 28 * abs(math.sin(t / 18))
    temperature = 26.5 + 4 * math.sin(t / 25) + random.uniform(-0.3, 0.3)
else:
    st.sidebar.markdown("---")
    humidity = st.sidebar.slider("💧 Simular humedad (%)", 0, 100, 45)
    temperature = st.sidebar.slider("🌡️ Simular temperatura (°C)", 18.0, 42.0, 28.0, 0.1)

humidity = round(humidity, 1)
temperature = round(temperature, 1)

# ── Determine status ──────────────────────────────────────────────────────────
wet = humidity > hum_threshold
temp_alert = temperature > temp_max or temperature < temp_min

if wet:
    status = "wet"
    status_label = "¡Pañal mojado!"
    status_desc = "Se detectó alta humedad. ¡Hora de cambiar al bebé! 👕"
    status_emoji = "💦"
else:
    status = "stable"
    status_label = "Bebé estable ✓"
    status_desc = "Todo bien. El pañal está seco y cómodo."
    status_emoji = "✨"

# Log history (max 8 entries, every ~5s in demo)
now = datetime.now()
if (now - st.session_state.last_update).seconds >= 5:
    st.session_state.history.insert(0, {
        "time": now.strftime("%H:%M:%S"),
        "status": status,
        "humidity": humidity,
        "temp": temperature,
    })
    st.session_state.history = st.session_state.history[:8]
    st.session_state.last_update = now

# ── RENDER ────────────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="bae-header">
  <div class="bae-title">BAE</div>
  <div class="bae-subtitle">Baby Ambient Eco-sensor</div>
  <div class="bae-eco-badge">🌿 Nano dispositivo ecológico</div>
</div>
""", unsafe_allow_html=True)

# Baby SVG
col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    st.markdown(
        f'<div style="text-align:center;margin:0.5rem 0">{BABY_CRY if wet else BABY_HAPPY}</div>',
        unsafe_allow_html=True
    )

# Status card
st.markdown(f"""
<div class="status-card {status}">
  <div style="font-size:2.2rem">{status_emoji}</div>
  <div class="status-label">{status_label}</div>
  <div class="status-desc">{status_desc}</div>
  {'<div style="margin-top:10px;font-size:0.8rem;font-weight:700;color:#8b1a1a;background:rgba(216,128,128,0.2);border-radius:10px;padding:4px 12px;display:inline-block">⚠️ Revisar temperatura</div>' if temp_alert else ''}
</div>
""", unsafe_allow_html=True)

# Metrics
hum_color = "#d88080" if wet else "#7ec4a4"
temp_color = "#d88080" if temp_alert else "#7ec4a4"

st.markdown(f"""
<div class="metrics-row">
  <div class="metric-chip">
    <div class="metric-icon">💧</div>
    <div class="metric-value" style="color:{hum_color}">{humidity}%</div>
    <div class="metric-label">Humedad</div>
  </div>
  <div class="metric-chip">
    <div class="metric-icon">🌡️</div>
    <div class="metric-value" style="color:{temp_color}">{temperature}°C</div>
    <div class="metric-label">Temperatura</div>
  </div>
  <div class="metric-chip">
    <div class="metric-icon">{'🔴' if wet else '🟢'}</div>
    <div class="metric-value" style="font-size:1rem;padding-top:4px">{'ALERTA' if wet else 'NORMAL'}</div>
    <div class="metric-label">Estado</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Humidity bar
pct = min(humidity / 100, 1.0)
bar_color = "#d88080" if wet else "#7ec4a4"
st.markdown(f"""
<div style="max-width:480px;margin:0 auto 1rem;background:white;border-radius:18px;padding:1.2rem 1.5rem;
     box-shadow:0 4px 16px rgba(0,0,0,0.06);border:2px solid #e8ede6;">
  <div style="font-family:'Fredoka One',cursive;font-size:0.9rem;color:#7a1e1e;margin-bottom:8px">
    Nivel de humedad del pañal
  </div>
  <div style="background:#f0f4ec;border-radius:20px;height:18px;overflow:hidden;">
    <div style="width:{pct*100:.0f}%;height:100%;background:{bar_color};border-radius:20px;
         transition:width 0.8s ease;"></div>
  </div>
  <div style="display:flex;justify-content:space-between;font-size:0.75rem;
       font-weight:700;color:#8fa89d;margin-top:5px">
    <span>Seco 0%</span>
    <span>Umbral {hum_threshold}%</span>
    <span>100% Saturado</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Divider
st.markdown('<hr class="bae-divider">', unsafe_allow_html=True)

# History
if st.session_state.history:
    rows_html = ""
    for entry in st.session_state.history:
        dot_cls = entry["status"]
        label = "Mojado 💦" if entry["status"] == "wet" else "Estable ✓"
        rows_html += f"""
        <div class="history-row">
          <div class="h-dot {dot_cls}"></div>
          <span>{label}</span>
          <span style="opacity:0.7;font-size:0.8rem">
            {entry['humidity']}% · {entry['temp']}°C
          </span>
          <span class="h-time">{entry['time']}</span>
        </div>"""
    st.markdown(f"""
    <div class="history-box">
      <div class="history-title">📋 Historial de lecturas</div>
      {rows_html}
    </div>
    """, unsafe_allow_html=True)

# Info cards
st.markdown("""
<div class="info-grid">
  <div class="info-card">
    <div class="info-card-title">🌿 Materiales eco</div>
    <p>PCB biodegradable · Sensor de fibra orgánica · Carcasa de bambú · Tinta vegetal conductora</p>
  </div>
  <div class="info-card">
    <div class="info-card-title">⚡ Nano dispositivo</div>
    <p>Peso: 1.2g · Tamaño: 18×12mm · Batería 72h · Conectividad BLE 5.0</p>
  </div>
  <div class="info-card">
    <div class="info-card-title">🌡️ Sensores</div>
    <p>Sensor resistivo de humedad + termistor NTC integrado en tejido del pañal</p>
  </div>
  <div class="info-card">
    <div class="info-card-title">📊 Precisión</div>
    <p>Humedad: ±2% · Temperatura: ±0.3°C · Muestreo cada 3 segundos</p>
  </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="bae-footer">
  BAE · Baby Ambient Eco-sensor · v1.0.0<br>
  Nano dispositivo ecológico integrado al pañal · Hecho con 🌿 y ❤️
</div>
""", unsafe_allow_html=True)

# Auto-refresh in demo mode
if demo_mode:
    time.sleep(3)
    st.rerun()
