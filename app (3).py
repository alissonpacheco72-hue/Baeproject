import streamlit as st
import time
import math
import random
from datetime import datetime

st.set_page_config(
    page_title="BAE · Baby Ambient Eco-sensor",
    page_icon="👶",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Fredoka+One&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background-color: #f0f4ec !important;
    font-family: 'Nunito', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }

.bae-header { text-align: center; padding: 28px 16px 12px; }
.bae-title {
    font-family: 'Fredoka One', cursive;
    font-size: 3.4rem; color: #7a1e1e;
    letter-spacing: 2px; line-height: 1;
}
.bae-sub {
    font-size: 0.78rem; color: #6b8f7e;
    font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; margin-top: 6px;
}
.bae-badge {
    display: inline-block; background: #7a1e1e; color: #f0f4ec;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 1.8px;
    padding: 3px 14px; border-radius: 20px; margin-top: 10px;
    text-transform: uppercase;
}

.baby-wrap {
    display: flex; justify-content: center; align-items: center;
    width: 100%; padding: 16px 0 8px;
}

.status-card {
    border-radius: 16px; padding: 20px 28px;
    margin: 12px auto; max-width: 480px;
    text-align: center; border-width: 2px; border-style: solid;
}
.status-card.stable { background: #d4ece2; border-color: #7ec4a4; }
.status-card.wet    { background: #fde4e4; border-color: #d88080; }
.status-emoji { font-size: 1.8rem; margin-bottom: 4px; }
.status-label {
    font-family: 'Fredoka One', cursive; font-size: 1.5rem; margin: 4px 0;
}
.stable .status-label { color: #1a6b4a; }
.wet    .status-label { color: #8b1a1a; }
.status-desc { font-size: 0.86rem; font-weight: 600; opacity: 0.72; }
.stable .status-desc { color: #1a6b4a; }
.wet    .status-desc { color: #8b1a1a; }
.temp-warn {
    display: inline-block; background: rgba(216,128,128,0.2);
    color: #8b1a1a; font-size: 0.76rem; font-weight: 700;
    padding: 3px 12px; border-radius: 8px; margin-top: 10px;
}

.metrics-grid {
    display: grid; grid-template-columns: 1fr 1fr 1fr;
    gap: 12px; max-width: 480px; margin: 12px auto;
}
.metric-card {
    background: #ffffff; border-radius: 14px;
    border: 2px solid #e4ede9; padding: 16px 12px; text-align: center;
}
.metric-icon { font-size: 1.3rem; line-height: 1; }
.metric-val {
    font-family: 'Fredoka One', cursive; font-size: 1.5rem;
    line-height: 1.1; margin-top: 4px;
}
.metric-lbl {
    font-size: 0.66rem; font-weight: 700; color: #8fa89d;
    text-transform: uppercase; letter-spacing: 1.4px; margin-top: 3px;
}

.hum-wrap {
    background: #ffffff; border-radius: 14px; border: 2px solid #e4ede9;
    padding: 16px 20px; max-width: 480px; margin: 12px auto;
}
.hum-title {
    font-family: 'Fredoka One', cursive; font-size: 0.9rem;
    color: #7a1e1e; margin-bottom: 10px;
}
.hum-track { background: #eef2ec; border-radius: 20px; height: 14px; overflow: hidden; }
.hum-fill  { height: 100%; border-radius: 20px; transition: width 0.6s ease; }
.hum-labels {
    display: flex; justify-content: space-between;
    font-size: 0.68rem; font-weight: 700; color: #96aaa3; margin-top: 6px;
}

.bae-divider {
    border: none; height: 2px; background: #d4e4de;
    max-width: 320px; margin: 18px auto; border-radius: 2px;
}

.history-card {
    background: #ffffff; border-radius: 14px; border: 2px solid #e4ede9;
    padding: 18px 20px; max-width: 480px; margin: 12px auto;
}
.history-title {
    font-family: 'Fredoka One', cursive; font-size: 0.95rem;
    color: #7a1e1e; margin-bottom: 12px;
}
.h-row {
    display: grid; grid-template-columns: 10px 1fr auto auto;
    align-items: center; gap: 10px;
    padding: 7px 0; border-bottom: 1px solid #eef2ec;
    font-size: 0.82rem; font-weight: 600; color: #4a6b5e;
}
.h-row:last-child { border-bottom: none; }
.h-dot { width: 10px; height: 10px; border-radius: 50%; }
.h-dot.stable { background: #7ec4a4; }
.h-dot.wet    { background: #d88080; }
.h-val  { color: #96aaa3; font-size: 0.76rem; text-align: right; }
.h-time { color: #b4c4be; font-size: 0.72rem; }

.info-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 12px; max-width: 480px; margin: 12px auto;
}
.info-card {
    background: #ffffff; border-radius: 14px;
    border: 2px solid #e4ede9; padding: 16px;
}
.info-title {
    font-family: 'Fredoka One', cursive; font-size: 0.88rem;
    color: #7a1e1e; margin-bottom: 6px;
}
.info-body {
    font-size: 0.78rem; color: #6b8f7e;
    font-weight: 600; line-height: 1.55;
}

.bae-footer {
    text-align: center; font-size: 0.7rem; color: #a8bdb5;
    font-weight: 700; padding: 20px 16px 28px; letter-spacing: 1px;
}

.stButton > button {
    background: #7a1e1e !important; color: #f0f4ec !important;
    border: none !important; border-radius: 50px !important;
    font-family: 'Fredoka One', cursive !important;
    font-size: 0.95rem !important; padding: 0.55rem 2rem !important;
}
.stButton > button:hover { background: #9a2e2e !important; }
</style>
""", unsafe_allow_html=True)

# ── Baby SVGs ──────────────────────────────────────────────────────────────────
BABY_HAPPY = """
<svg width="160" height="170" viewBox="0 0 160 170" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes breathe{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
@keyframes blink{0%,88%,100%{transform:scaleY(1)}94%{transform:scaleY(0.08)}}
@keyframes wag{0%,100%{transform:rotate(-6deg)}50%{transform:rotate(6deg)}}
.body{transform-origin:80px 120px;animation:breathe 2.8s ease-in-out infinite}
.eye-l{transform-origin:60px 78px;animation:blink 4.5s ease-in-out infinite}
.eye-r{transform-origin:100px 78px;animation:blink 4.5s ease-in-out infinite 0.15s}
.curl{transform-origin:80px 36px;animation:wag 3.2s ease-in-out infinite}
</style>
<ellipse cx="80" cy="95" rx="68" ry="78" fill="#aed9cc" opacity="0.45"/>
<g class="body">
  <path d="M56 118 Q80 138 104 118 L106 144 Q80 160 54 144 Z"
        fill="#f8f5f0" stroke="#7a1e1e" stroke-width="2.2" stroke-linejoin="round"/>
  <circle cx="80" cy="134" r="4.5" fill="none" stroke="#7a1e1e" stroke-width="1.8"/>
  <ellipse cx="80" cy="114" rx="28" ry="16" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2"/>
  <ellipse cx="34" cy="76" rx="8" ry="10" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2"/>
  <ellipse cx="126" cy="76" rx="8" ry="10" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2"/>
  <circle cx="80" cy="68" r="40" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2.2"/>
  <g class="curl">
    <path d="M73 34 Q70 24 80 22 Q90 20 90 30 Q90 37 82 37"
          fill="none" stroke="#7a1e1e" stroke-width="2.5" stroke-linecap="round"/>
  </g>
  <g class="eye-l">
    <path d="M52 76 Q60 68 68 76" fill="none" stroke="#7a1e1e" stroke-width="2.8" stroke-linecap="round"/>
  </g>
  <g class="eye-r">
    <path d="M92 76 Q100 68 108 76" fill="none" stroke="#7a1e1e" stroke-width="2.8" stroke-linecap="round"/>
  </g>
  <ellipse cx="52" cy="85" rx="9" ry="6" fill="#f4a0a0" opacity="0.5"/>
  <ellipse cx="108" cy="85" rx="9" ry="6" fill="#f4a0a0" opacity="0.5"/>
  <path d="M64 92 Q80 104 96 92" fill="none" stroke="#7a1e1e" stroke-width="2.5" stroke-linecap="round"/>
</g>
</svg>"""

BABY_CRY = """
<svg width="160" height="170" viewBox="0 0 160 170" xmlns="http://www.w3.org/2000/svg">
<style>
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-3px)}75%{transform:translateX(3px)}}
@keyframes tearL{0%{transform:translateY(0);opacity:1}100%{transform:translateY(24px);opacity:0}}
@keyframes tearR{0%{transform:translateY(0);opacity:1}100%{transform:translateY(20px);opacity:0}}
.body{transform-origin:80px 90px;animation:shake 0.5s ease-in-out infinite}
.tl{animation:tearL 1.1s ease-in infinite}
.tr{animation:tearR 1.1s ease-in infinite 0.35s}
</style>
<ellipse cx="80" cy="95" rx="68" ry="78" fill="#f5c5c5" opacity="0.35"/>
<g class="body">
  <path d="M56 118 Q80 138 104 118 L106 144 Q80 160 54 144 Z"
        fill="#f8f5f0" stroke="#7a1e1e" stroke-width="2.2" stroke-linejoin="round"/>
  <circle cx="80" cy="134" r="4.5" fill="none" stroke="#7a1e1e" stroke-width="1.8"/>
  <ellipse cx="80" cy="114" rx="28" ry="16" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2"/>
  <ellipse cx="34" cy="76" rx="8" ry="10" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2"/>
  <ellipse cx="126" cy="76" rx="8" ry="10" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2"/>
  <circle cx="80" cy="68" r="40" fill="#fce8d8" stroke="#7a1e1e" stroke-width="2.2"/>
  <path d="M73 34 Q70 24 80 22 Q90 20 90 30 Q90 37 82 37"
        fill="none" stroke="#7a1e1e" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M51 63 Q60 57 68 63" fill="none" stroke="#7a1e1e" stroke-width="2" stroke-linecap="round"/>
  <path d="M92 63 Q100 57 109 63" fill="none" stroke="#7a1e1e" stroke-width="2" stroke-linecap="round"/>
  <ellipse cx="60" cy="76" rx="5.5" ry="6.5" fill="#7a1e1e"/>
  <ellipse cx="100" cy="76" rx="5.5" ry="6.5" fill="#7a1e1e"/>
  <ellipse cx="58" cy="73" rx="1.8" ry="2.2" fill="white"/>
  <ellipse cx="98" cy="73" rx="1.8" ry="2.2" fill="white"/>
  <ellipse cx="52" cy="86" rx="10" ry="7" fill="#e87070" opacity="0.4"/>
  <ellipse cx="108" cy="86" rx="10" ry="7" fill="#e87070" opacity="0.4"/>
  <path d="M64 96 Q80 88 96 96" fill="none" stroke="#7a1e1e" stroke-width="2.5" stroke-linecap="round"/>
  <g class="tl">
    <path d="M57 83 Q55 91 57 98" fill="none" stroke="#6aaad4" stroke-width="2.5" stroke-linecap="round"/>
  </g>
  <g class="tr">
    <path d="M103 83 Q105 91 103 98" fill="none" stroke="#6aaad4" stroke-width="2.5" stroke-linecap="round"/>
  </g>
  <ellipse cx="68" cy="146" rx="5" ry="6" fill="#6aaad4" opacity="0.4"/>
  <ellipse cx="80" cy="150" rx="4" ry="5" fill="#6aaad4" opacity="0.32"/>
  <ellipse cx="92" cy="146" rx="4.5" ry="5.5" fill="#6aaad4" opacity="0.38"/>
</g>
</svg>"""

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuración BAE")
    hum_threshold = st.slider("💧 Umbral humedad (%)", 40, 90, 65)
    temp_max      = st.slider("🌡️ Temperatura máx (°C)", 32, 40, 36)
    temp_min      = st.slider("❄️ Temperatura mín (°C)", 20, 30, 24)
    st.markdown("---")
    st.markdown("**Materiales ecológicos:**")
    st.caption("🌿 PCB biodegradable · Sensor orgánico\nCarcasa bambú · Tinta vegetal")
    demo_mode = st.toggle("🎮 Modo demostración", value=True)

# ── State ──────────────────────────────────────────────────────────────────────
if "history"  not in st.session_state: st.session_state.history  = []
if "last_log" not in st.session_state: st.session_state.last_log = datetime.now()

# ── Sensor values ──────────────────────────────────────────────────────────────
if demo_mode:
    t           = time.time()
    humidity    = round(45 + 28 * abs(math.sin(t / 18)), 1)
    temperature = round(26.5 + 4 * math.sin(t / 25) + random.uniform(-0.2, 0.2), 1)
else:
    humidity    = st.sidebar.slider("💧 Humedad (%)",      0,    100, 45)
    temperature = st.sidebar.slider("🌡️ Temperatura (°C)", 18.0, 42.0, 28.0, 0.1)

wet        = humidity    > hum_threshold
temp_alert = temperature > temp_max or temperature < temp_min

status_cls   = "wet"            if wet else "stable"
status_label = "¡Pañal mojado!" if wet else "Bebé estable"
status_desc  = "Alta humedad — cambiar pañal" if wet else "Pañal seco y cómodo"
status_emoji = "💦"             if wet else "✨"

now = datetime.now()
if (now - st.session_state.last_log).seconds >= 5:
    st.session_state.history.insert(0, {
        "time": now.strftime("%H:%M:%S"),
        "status": status_cls, "hum": humidity, "temp": temperature,
    })
    st.session_state.history = st.session_state.history[:8]
    st.session_state.last_log = now

# ── RENDER ─────────────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="bae-header">
  <div class="bae-title">BAE</div>
  <div class="bae-sub">Baby Ambient Eco-sensor</div>
  <div class="bae-badge">🌿 Nano dispositivo ecológico</div>
</div>
""", unsafe_allow_html=True)

# Baby — centrado
st.markdown(
    f'<div class="baby-wrap">{BABY_CRY if wet else BABY_HAPPY}</div>',
    unsafe_allow_html=True
)

# Status card
warn = '<div class="temp-warn">⚠️ Revisar temperatura</div>' if temp_alert else ""
st.markdown(f"""
<div class="status-card {status_cls}">
  <div class="status-emoji">{status_emoji}</div>
  <div class="status-label">{status_label}</div>
  <div class="status-desc">{status_desc}</div>
  {warn}
</div>
""", unsafe_allow_html=True)

# Metrics 3 cols
hc = "#d88080" if wet        else "#1a6b4a"
tc = "#d88080" if temp_alert else "#1a6b4a"
sc = "#d88080" if wet        else "#1a6b4a"
sl = "ALERTA"  if wet        else "NORMAL"
st.markdown(f"""
<div class="metrics-grid">
  <div class="metric-card">
    <div class="metric-icon">💧</div>
    <div class="metric-val" style="color:{hc}">{humidity}%</div>
    <div class="metric-lbl">Humedad</div>
  </div>
  <div class="metric-card">
    <div class="metric-icon">🌡️</div>
    <div class="metric-val" style="color:{tc}">{temperature}°C</div>
    <div class="metric-lbl">Temperatura</div>
  </div>
  <div class="metric-card">
    <div class="metric-icon">{'🔴' if wet else '🟢'}</div>
    <div class="metric-val" style="color:{sc};font-size:1rem;padding-top:6px">{sl}</div>
    <div class="metric-lbl">Estado</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Humidity bar
pct = min(humidity / 100.0, 1.0)
bc  = "#d88080" if wet else "#7ec4a4"
st.markdown(f"""
<div class="hum-wrap">
  <div class="hum-title">Nivel de humedad del pañal</div>
  <div class="hum-track">
    <div class="hum-fill" style="width:{pct*100:.0f}%;background:{bc}"></div>
  </div>
  <div class="hum-labels">
    <span>Seco — 0%</span>
    <span>Umbral {hum_threshold}%</span>
    <span>100% — Saturado</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Divider
st.markdown('<hr class="bae-divider">', unsafe_allow_html=True)

# History
if st.session_state.history:
    rows = "".join(f"""
    <div class="h-row">
      <div class="h-dot {e['status']}"></div>
      <span>{'Mojado 💦' if e['status']=='wet' else 'Estable ✓'}</span>
      <span class="h-val">{e['hum']}% · {e['temp']}°C</span>
      <span class="h-time">{e['time']}</span>
    </div>""" for e in st.session_state.history)
    st.markdown(f"""
    <div class="history-card">
      <div class="history-title">📋 Historial de lecturas</div>
      {rows}
    </div>""", unsafe_allow_html=True)

# Info 2×2 grid
st.markdown("""
<div class="info-grid">
  <div class="info-card">
    <div class="info-title">🌿 Materiales eco</div>
    <div class="info-body">PCB biodegradable · Sensor de fibra orgánica · Carcasa bambú · Tinta vegetal conductora</div>
  </div>
  <div class="info-card">
    <div class="info-title">⚡ Nano dispositivo</div>
    <div class="info-body">Peso: 1.2 g · Tamaño: 18 × 12 mm · Batería 72 h · BLE 5.0</div>
  </div>
  <div class="info-card">
    <div class="info-title">🔬 Sensores</div>
    <div class="info-body">Sensor resistivo orgánico + termistor NTC integrado en el tejido del pañal</div>
  </div>
  <div class="info-card">
    <div class="info-title">📊 Precisión</div>
    <div class="info-body">Humedad ±2% · Temperatura ±0.3 °C · Muestreo cada 3 s</div>
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

if demo_mode:
    time.sleep(3)
    st.rerun()
