import streamlit as st
import time
import random
import math
from datetime import datetime, timedelta

st.set_page_config(
    page_title="BAE · Baby Ambient Eco-sensor",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Fredoka+One&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background-color: #fdf6f0 !important;
    font-family: 'Nunito', sans-serif;
}
[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stSidebar"] { background: #fff8f4 !important; border-right: 2px solid #f0ddd4; }
#MainMenu, footer { visibility: hidden; }
.bae-logo-B { font-family:'Fredoka One',cursive; font-size:2.8rem; color:#7aaebd; line-height:1; display:inline; }
.bae-logo-a { font-family:'Fredoka One',cursive; font-size:2.2rem; color:#9baf8a; line-height:1; display:inline; }
.bae-logo-e { font-family:'Fredoka One',cursive; font-size:2.2rem; color:#e8968a; line-height:1; display:inline; }
.baby-chip {
    display:flex; align-items:center; gap:10px;
    background:white; border:2px solid #f0ddd4; border-radius:50px;
    padding:6px 16px 6px 6px; box-shadow:0 2px 12px rgba(0,0,0,0.06);
    float:right;
}
.baby-chip-name { font-weight:900; font-size:1rem; color:#5a3a2a; line-height:1.1; }
.baby-chip-sub  { font-size:0.75rem; color:#b08878; font-weight:600; }
.status-pill { display:inline-flex; align-items:center; gap:5px; font-size:0.78rem;
    font-weight:700; padding:4px 12px; border-radius:20px; }
.status-pill.ok   { background:#e8f5ef; color:#1a6b4a; }
.status-pill.warn { background:#fde8e8; color:#8b1a1a; }
.dcard {
    background:white; border-radius:20px; padding:1.2rem 1.3rem;
    border:2px solid #f0ddd4; box-shadow:0 3px 18px rgba(160,100,80,0.08);
    height:100%; position:relative; overflow:hidden;
}
.dcard-title { font-size:0.82rem; font-weight:700; color:#b08878;
    text-transform:uppercase; letter-spacing:1.5px; margin-bottom:0.5rem; }
.big-value { font-family:'Fredoka One',cursive; font-size:2.6rem; color:#5a3a2a; line-height:1; }
.big-unit  { font-size:1rem; color:#b08878; font-weight:700; }
.sub-text  { font-size:0.78rem; color:#c0a090; font-weight:600; margin-top:4px; }
.alert-item {
    display:flex; align-items:flex-start; gap:8px; padding:8px 10px;
    border-radius:12px; margin-bottom:7px; font-size:0.82rem; font-weight:700;
}
.alert-item.red { background:#fde8e8; color:#8b1a1a; }
.alert-item.yel { background:#fef9e7; color:#7d6000; }
.alert-item.gre { background:#e8f5ef; color:#1a5c3a; }
.adot { width:8px; height:8px; border-radius:50%; flex-shrink:0; margin-top:3px; }
.adot-red { background:#e24b4a; }
.adot-yel { background:#f0a500; }
.adot-gre { background:#1d9e75; }
.mini-bars { display:flex; align-items:flex-end; gap:3px; height:44px; margin-top:8px; }
.mini-bar  { flex:1; border-radius:4px 4px 0 0; background:linear-gradient(180deg,#e8968a,#f5c5b8); min-height:4px; }
.drops { display:flex; gap:6px; justify-content:center; margin:0.5rem 0; }
.drop    { width:22px; height:28px; background:#7aaebd; border-radius:50% 50% 50% 50%/40% 40% 60% 60%; opacity:0.85; }
.drop.sm { width:15px; height:19px; opacity:0.6; }
.hist-row { display:flex; align-items:center; gap:10px; padding:7px 0;
    border-bottom:1px solid #f5ede8; font-size:0.82rem; font-weight:700; color:#5a3a2a; }
.hist-row:last-child { border-bottom:none; }
.hist-time { color:#c0a090; font-size:0.75rem; margin-left:auto; }
.section-head { font-size:1.05rem; font-weight:900; color:#5a3a2a;
    margin:1rem 0 0.7rem; border-bottom:2px dashed #f0ddd4; padding-bottom:5px; }
.cuento-card { background:#fff8f4; border:2px dashed #e8c5b4; border-radius:20px;
    padding:1rem 1.2rem; font-size:0.88rem; color:#8b6050; font-weight:600;
    font-style:italic; line-height:1.6; }
.eco-badge { display:inline-block; background:#e8f5ef; color:#1a6b4a; font-size:0.72rem;
    font-weight:700; padding:3px 10px; border-radius:20px; margin:3px 2px; }
.stButton>button {
    background:#e8968a !important; color:white !important; border:none !important;
    border-radius:50px !important; font-family:'Fredoka One',cursive !important;
    font-size:1rem !important; padding:0.5rem 1.8rem !important;
    box-shadow:0 3px 12px rgba(232,150,138,0.4) !important;
}
.stButton>button:hover { background:#d4756a !important; transform:translateY(-1px) !important; }
[data-testid="stSidebar"] label {
    font-family:'Nunito',sans-serif !important; font-weight:700 !important;
    color:#8b5e50 !important; font-size:0.85rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Baby SVGs ─────────────────────────────────────────────────────────────────
HAPPY = """<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <circle cx="24" cy="26" r="20" fill="#fce8d8"/>
  <ellipse cx="6" cy="27" rx="5" ry="7" fill="#fce8d8"/>
  <ellipse cx="42" cy="27" rx="5" ry="7" fill="#fce8d8"/>
  <path d="M20 22 Q24 17 28 22" fill="none" stroke="#7a4030" stroke-width="2" stroke-linecap="round"/>
  <path d="M16 32 Q24 39 32 32" fill="none" stroke="#7a4030" stroke-width="2.2" stroke-linecap="round"/>
  <ellipse cx="15" cy="32" rx="5" ry="3.5" fill="#f4a090" opacity="0.5"/>
  <ellipse cx="33" cy="32" rx="5" ry="3.5" fill="#f4a090" opacity="0.5"/>
  <path d="M21 10 Q20 5 24 4 Q28 3 28 8 Q28 12 25 12" fill="none" stroke="#c8905a" stroke-width="2" stroke-linecap="round"/>
</svg>"""

CRY = """<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <circle cx="24" cy="26" r="20" fill="#fce8d8"/>
  <ellipse cx="6" cy="27" rx="5" ry="7" fill="#fce8d8"/>
  <ellipse cx="42" cy="27" rx="5" ry="7" fill="#fce8d8"/>
  <ellipse cx="19" cy="25" rx="4" ry="5" fill="#5a3060"/>
  <ellipse cx="29" cy="25" rx="4" ry="5" fill="#5a3060"/>
  <path d="M16 35 Q24 30 32 35" fill="none" stroke="#7a4030" stroke-width="2.2" stroke-linecap="round"/>
  <ellipse cx="14" cy="33" rx="6" ry="4" fill="#e87070" opacity="0.4"/>
  <ellipse cx="34" cy="33" rx="6" ry="4" fill="#e87070" opacity="0.4"/>
  <path d="M18 30 Q17 36 18 40" fill="none" stroke="#7aaebd" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M30 30 Q31 36 30 40" fill="none" stroke="#7aaebd" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M21 10 Q20 5 24 4 Q28 3 28 8 Q28 12 25 12" fill="none" stroke="#c8905a" stroke-width="2" stroke-linecap="round"/>
</svg>"""

def gauge_svg(temp, t_min, t_max):
    rng = t_max - t_min or 1
    pct = max(0.0, min(1.0, (temp - t_min) / rng))
    arc_len = 204
    offset  = round(arc_len * (1 - pct))
    angle   = math.pi - pct * math.pi
    nx = round(80 + 58 * math.cos(angle), 1)
    ny = round(85 - 58 * math.sin(angle), 1)
    col = "#e24b4a" if temp > t_max else ("#7aaebd" if temp < t_min else "#9baf8a")
    return f"""<svg width="160" height="95" viewBox="0 0 160 95" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="gg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#7aaebd"/>
    <stop offset="55%" stop-color="#9baf8a"/>
    <stop offset="80%" stop-color="#f0a500"/>
    <stop offset="100%" stop-color="#e24b4a"/>
  </linearGradient></defs>
  <path d="M15 85 A65 65 0 0 1 145 85" fill="none" stroke="#f0ddd4" stroke-width="14" stroke-linecap="round"/>
  <path d="M15 85 A65 65 0 0 1 145 85" fill="none" stroke="url(#gg)" stroke-width="14"
        stroke-linecap="round" stroke-dasharray="{arc_len}" stroke-dashoffset="{offset}"/>
  <circle cx="{nx}" cy="{ny}" r="7" fill="{col}"/>
  <circle cx="{nx}" cy="{ny}" r="4" fill="white"/>
</svg>"""

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("history", []), ("last_update", datetime.now() - timedelta(seconds=10)),
             ("baby_name", "Emma"), ("baby_age", "6 meses"),
             ("baby_weight", 7.5), ("baby_sex", "Niña 👧")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<span class="bae-logo-B">B</span><span class="bae-logo-a">a</span><span class="bae-logo-e">e</span>', unsafe_allow_html=True)
    st.markdown("### 👶 Perfil del bebé")

    name   = st.text_input("Nombre", value=st.session_state.baby_name, placeholder="Ej: Emma")
    age    = st.text_input("Edad",   value=st.session_state.baby_age,  placeholder="Ej: 6 meses")
    weight = st.number_input("Peso (kg)", value=st.session_state.baby_weight,
                              min_value=1.0, max_value=30.0, step=0.1, format="%.1f")
    sex    = st.selectbox("Sexo", ["Niña 👧", "Niño 👦", "Otro"],
                           index=["Niña 👧","Niño 👦","Otro"].index(st.session_state.baby_sex)
                           if st.session_state.baby_sex in ["Niña 👧","Niño 👦","Otro"] else 0)

    if st.button("💾 Guardar perfil"):
        st.session_state.baby_name   = name
        st.session_state.baby_age    = age
        st.session_state.baby_weight = weight
        st.session_state.baby_sex    = sex
        st.success(f"¡Perfil de {name} guardado! 🎉")

    st.markdown("---")
    st.markdown("### ⚙️ Umbrales del sensor")
    hum_threshold = st.slider("💧 Humedad máx (%)", 40, 90, 65)
    temp_max      = st.slider("🌡️ Temp máx (°C)",  34, 40, 37)
    temp_min      = st.slider("❄️ Temp mín (°C)",  18, 30, 24)
    st.markdown("---")
    demo_mode = st.toggle("🎮 Modo demostración", value=True)
    if not demo_mode:
        m_hum  = st.slider("Humedad manual (%)", 0, 100, 45)
        m_temp = st.slider("Temp manual (°C)", 18.0, 42.0, 28.5, 0.1)
    st.markdown("---")
    st.markdown("**🌿 Nano dispositivo ecológico**")
    st.markdown("""<span class="eco-badge">PCB biodegradable</span>
<span class="eco-badge">Sensor orgánico</span>
<span class="eco-badge">Bambú</span>
<span class="eco-badge">BLE 5.0</span>
<span class="eco-badge">1.2g · 18×12mm</span>""", unsafe_allow_html=True)

# ── Sensor readings ───────────────────────────────────────────────────────────
t_now = time.time()
if demo_mode:
    humidity    = round(45 + 28 * abs(math.sin(t_now / 18)), 1)
    temperature = round(35.5 + 2.5 * math.sin(t_now / 25) + random.uniform(-0.2, 0.2), 1)
else:
    humidity    = float(m_hum)
    temperature = round(float(m_temp), 1)

wet       = humidity > hum_threshold
temp_warn = temperature > temp_max or temperature < temp_min
all_ok    = not wet and not temp_warn

# Log history
now = datetime.now()
if (now - st.session_state.last_update).seconds >= 5:
    st.session_state.history.insert(0, {
        "time": now.strftime("%H:%M:%S"), "wet": wet,
        "status": "Mojado 💦" if wet else "Estable ✓",
        "humidity": humidity, "temp": temperature,
    })
    st.session_state.history = st.session_state.history[:14]
    st.session_state.last_update = now

random.seed(7)
hist24 = [round(35.5 + 2 * math.sin(i / 2.5) + random.uniform(-0.4, 0.4), 1) for i in range(14)]

# ── TOP BAR ───────────────────────────────────────────────────────────────────
c_logo, c_head, c_space, c_chip = st.columns([0.8, 2.5, 1.5, 2.2])

with c_logo:
    st.markdown('<span class="bae-logo-B">B</span><span class="bae-logo-a">a</span><span class="bae-logo-e">e</span>', unsafe_allow_html=True)

with c_head:
    pill_cls = "ok" if all_ok else "warn"
    pill_txt = "🟢 Temperatura estable" if all_ok else ("🔴 Pañal mojado" if wet else "🟡 Revisar temperatura")
    st.markdown(f"""
    <div style="padding-top:0.5rem">
      <div class="section-head" style="border:none;margin:0;font-size:1.2rem">Panel de bienestar</div>
      <span class="status-pill {pill_cls}">{pill_txt}</span>
    </div>""", unsafe_allow_html=True)

with c_chip:
    face_svg = CRY if wet else HAPPY
    st.markdown(f"""
    <div class="baby-chip" style="float:right;margin-top:0.2rem">
      {face_svg}
      <div>
        <div class="baby-chip-name">{st.session_state.baby_name}</div>
        <div class="baby-chip-sub">{st.session_state.baby_age} · {st.session_state.baby_weight} kg</div>
      </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

# ── ROW 1 ─────────────────────────────────────────────────────────────────────
r1a, r1b, r1c = st.columns([1.2, 1.2, 1])

# Temperature
with r1a:
    t_color = "#e24b4a" if temp_warn else "#5a3a2a"
    st.markdown(f"""
    <div class="dcard">
      <div class="dcard-title">🌡️ Temperatura corporal</div>
      <div style="text-align:center">{gauge_svg(temperature, temp_min, temp_max)}</div>
      <div style="text-align:center;margin-top:-8px">
        <span class="big-value" style="color:{t_color}">{temperature}</span>
        <span class="big-unit">°C</span>
      </div>
      <div class="sub-text" style="text-align:center">Rango normal: {temp_min}–{temp_max} °C</div>
      <div style="margin-top:8px;background:#f5ede8;border-radius:12px;padding:7px 10px">
        <div class="sub-text">📋 Última alerta: {hist24[0]} °C</div>
      </div>
      <div style="text-align:center;margin-top:10px">
        <span style="background:#f0f8f5;border:2px solid #d0e8d8;border-radius:20px;
              padding:5px 14px;font-size:0.78rem;font-weight:700;color:#1a6b4a;cursor:pointer">
          📄 Ver historial
        </span>
      </div>
    </div>""", unsafe_allow_html=True)

# Humidity
with r1b:
    n_d = min(3, max(1, int(humidity / 34) + 1))
    d_html = "".join(['<div class="drop"></div>'] * n_d)
    if humidity > 55: d_html += '<div class="drop sm"></div>'
    h_color = "#e24b4a" if wet else "#7aaebd"
    st.markdown(f"""
    <div class="dcard">
      <div class="dcard-title">💧 Humedad ambiental</div>
      <div class="drops" style="margin-top:1.2rem">{d_html}</div>
      <div style="text-align:center;margin-top:0.2rem">
        <span class="big-value" style="color:{h_color}">{humidity}</span>
        <span class="big-unit">%</span>
      </div>
      <div style="background:#f5ede8;border-radius:20px;height:10px;overflow:hidden;margin-top:12px">
        <div style="width:{min(humidity,100):.0f}%;height:100%;background:{h_color};border-radius:20px;transition:width 0.8s ease"></div>
      </div>
      <div style="display:flex;justify-content:space-between;margin-top:4px">
        <span class="sub-text">0%</span>
        <span class="sub-text">↑ {hum_threshold}%</span>
        <span class="sub-text">100%</span>
      </div>
      <div class="sub-text" style="margin-top:8px;{'color:#e24b4a' if wet else ''}">
        {'⚠️ Pañal mojado · Cambio necesario' if wet else '✅ Pañal en buen estado'}
      </div>
    </div>""", unsafe_allow_html=True)

# Alerts
with r1c:
    alerts = []
    if wet:
        alerts.append(("red","adot-red","Pañal mojado detectado. ¡Cambio necesario!"))
    if temperature > temp_max:
        alerts.append(("red","adot-red",f"Temperatura elevada durante la noche."))
    if temperature < temp_min:
        alerts.append(("yel","adot-yel","Temperatura baja. Abriga al bebé."))
    if humidity > hum_threshold * 0.75 and not wet:
        alerts.append(("yel","adot-yel","Nivel de humedad bajo. Revisa el entorno."))
    if not alerts:
        alerts.append(("gre","adot-gre","Todo bien. El bebé está cómodo."))
        alerts.append(("gre","adot-gre","Temperatura estable en rango normal."))
    al_html = "".join([f'<div class="alert-item {c}"><div class="adot {d}"></div><span>{m}</span></div>'
                       for c,d,m in alerts])
    st.markdown(f'<div class="dcard"><div class="dcard-title">🔔 Alertas</div><div style="margin-top:0.5rem">{al_html}</div></div>',
                unsafe_allow_html=True)

st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

# ── ROW 2 ─────────────────────────────────────────────────────────────────────
r2a, r2b, r2c = st.columns([1, 1.2, 1])

# 24h chart
with r2a:
    mx = max(hist24); mn = min(hist24); rng2 = mx - mn or 1
    bars = "".join([f'<div class="mini-bar" style="height:{int(((v-mn)/rng2)*38)+6}px"></div>' for v in hist24])
    recent = st.session_state.history[:3]
    rows_h = "".join([
        f'<div class="hist-row">'
        f'<span style="color:{"#e24b4a" if r["wet"] else "#1d9e75"}">{"💦" if r["wet"] else "✓"}</span>'
        f'<span>{r["temp"]}°C&nbsp;·&nbsp;{r["humidity"]}%</span>'
        f'<span class="hist-time">{r["time"]}</span></div>'
        for r in recent
    ]) or '<div class="sub-text">Sin registros aún...</div>'
    st.markdown(f"""
    <div class="dcard">
      <div class="dcard-title">📈 Últimas 24 horas</div>
      <div class="mini-bars">{bars}</div>
      <div style="margin-top:1rem">{rows_h}</div>
    </div>""", unsafe_allow_html=True)

# Tips / cuentos
tips = [
    ("Cuentos 🌙", f"Érase una vez un bebé llamado {st.session_state.baby_name} que dormía plácidamente gracias a BAE, su nano guardián ecológico. Cada noche, mientras las estrellas brillaban, BAE vigilaba su temperatura y humedad..."),
    ("Tip del día 💡", f"Cambia el pañal de {st.session_state.baby_name} cada 2-3 horas aunque parezca seco. La piel del bebé lo agradecerá. BAE te avisa antes de que haya incomodidad."),
    ("¿Sabías que? 🌱", "El dispositivo BAE está hecho con PCB biodegradable y sensor de fibra orgánica. Pesa solo 1.2g y dura 72h con una sola carga. ¡Tecnología con conciencia!"),
]
tip_idx  = int(t_now / 20) % len(tips)
tip_name, tip_body = tips[tip_idx]
with r2b:
    st.markdown(f"""
    <div class="dcard">
      <div class="dcard-title">{tip_name}</div>
      <div class="cuento-card" style="margin-top:0.5rem">
        <div style="font-family:'Fredoka One',cursive;font-size:1.1rem;color:#e8968a;
             margin-bottom:6px;font-style:normal">{tip_name}</div>
        {tip_body}
      </div>
      <div class="sub-text" style="margin-top:8px;text-align:center">
        🌿 BAE · Cuida al bebé, cuida el planeta
      </div>
    </div>""", unsafe_allow_html=True)

# Last record
with r2c:
    lh = st.session_state.history[0] if st.session_state.history else None
    l_time = lh["time"] if lh else "--:--"
    l_temp = lh["temp"] if lh else "--"
    l_hum  = lh["humidity"] if lh else "--"
    today  = datetime.now().strftime("%d de %b")
    st.markdown(f"""
    <div class="dcard">
      <div class="dcard-title">📡 Último registro</div>
      <div style="background:#f5ede8;border-radius:14px;padding:10px 14px;margin:8px 0">
        <div class="sub-text">{today} · {l_time}</div>
        <div style="font-family:'Fredoka One',cursive;font-size:1.5rem;color:#5a3a2a">{l_temp}°C</div>
      </div>
      <div style="display:flex;gap:8px;margin-bottom:8px">
        <div style="background:#e8f5ef;border-radius:14px;padding:8px;flex:1;text-align:center">
          <div class="sub-text">🌡️ Temp</div>
          <div style="font-weight:900;color:#1a6b4a">{l_temp}°C</div>
        </div>
        <div style="background:#e8f0fb;border-radius:14px;padding:8px;flex:1;text-align:center">
          <div class="sub-text">💧 Hum</div>
          <div style="font-weight:900;color:#185fa5">{l_hum}%</div>
        </div>
      </div>
      <div class="sub-text">🔵 Dispositivo: <b style="color:#7aaebd">Conectado</b></div>
      <div class="sub-text" style="font-family:monospace;font-size:0.7rem;margin-top:3px">ID: 0x1234…5def</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

# ── ROW 3: Historial ──────────────────────────────────────────────────────────
st.markdown('<div class="section-head">📋 Historial de lecturas</div>', unsafe_allow_html=True)
if st.session_state.history:
    rows = "".join([
        f'<div class="hist-row">'
        f'<div style="width:10px;height:10px;border-radius:50%;background:{"#e24b4a" if e["wet"] else "#1d9e75"};flex-shrink:0"></div>'
        f'<span style="min-width:110px">{e["status"]}</span>'
        f'<span style="color:#8b6050">🌡️ {e["temp"]}°C</span>'
        f'<span style="color:#7aaebd">💧 {e["humidity"]}%</span>'
        f'<span class="hist-time">{e["time"]}</span></div>'
        for e in st.session_state.history
    ])
    st.markdown(f'<div class="dcard" style="max-height:200px;overflow-y:auto">{rows}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="dcard sub-text">Aún no hay registros. Esperando datos del dispositivo...</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:1.5rem 0 0.5rem;color:#c0a090;font-weight:700;font-size:0.75rem">
  <span class="bae-logo-B" style="font-size:1.2rem">B</span>
  <span class="bae-logo-a" style="font-size:1rem">a</span>
  <span class="bae-logo-e" style="font-size:1rem">e</span>
  &nbsp;· Baby Ambient Eco-sensor v2.0 · Cuidando a {st.session_state.baby_name} con 🌿 y ❤️
</div>""", unsafe_allow_html=True)

if demo_mode:
    time.sleep(3)
    st.rerun()
