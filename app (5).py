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

# ─────────────────────────────────────────────────────────────────────────────
#  CSS  – paleta exacta del logo: azul #7ab3c8 · sage #8fa882 · coral #e8907a
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Fredoka+One&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

html,body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"]>.main{
    background-color:#f5f0eb !important;
    font-family:'Nunito',sans-serif;
}
[data-testid="stHeader"]{background:transparent !important}
#MainMenu,footer,header{visibility:hidden}
[data-testid="stVerticalBlock"]{gap:0 !important}

/* ── Topbar ── */
.topbar{display:flex;justify-content:space-between;align-items:center;padding:16px 0 10px}
.baby-profile{
    display:flex;align-items:center;gap:8px;cursor:pointer;
    background:#fff;border:2.5px solid #e8907a;border-radius:40px;
    padding:5px 14px 5px 5px;transition:all .2s;
}
.baby-profile:hover{background:#fdf5f2}
.avatar-sm{
    width:36px;height:36px;border-radius:50%;
    background:#fce8d8;border:2px solid #e8907a;
    display:flex;align-items:center;justify-content:center;overflow:hidden;
}
.baby-name{font-weight:800;font-size:.82rem;color:#2d2016;line-height:1.1}
.baby-age {font-size:.68rem;color:#e8907a;font-weight:600}
.spill{
    display:inline-flex;align-items:center;gap:5px;
    font-size:.7rem;font-weight:700;color:#1a6b4a;
    background:#d4ece2;padding:3px 10px;border-radius:20px;
}
.sdot{width:7px;height:7px;border-radius:50%;background:#8fa882;animation:pdot 2s ease-in-out infinite}
.spill.alert{color:#7a1e1e;background:#fde4e4}
.spill.alert .sdot{background:#e8907a}
@keyframes pdot{0%,100%{opacity:1}50%{opacity:.3}}

/* ── HERO ── */
.hero{
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    background:#fff;border:2.5px solid #7ab3c8;border-radius:22px;
    padding:18px 12px 12px;margin:0 0 12px;position:relative;overflow:hidden;
}
.hero::before{
    content:'';position:absolute;inset:0;
    background:radial-gradient(ellipse at 50% 40%,rgba(122,179,200,.13) 0%,transparent 70%);
    pointer-events:none;
}
.hero-lbl{font-family:'Fredoka One',cursive;font-size:1.05rem;margin-top:6px;transition:color .4s}
.hero-sub{font-size:.74rem;font-weight:600;margin-top:2px;opacity:.75;transition:color .4s}
.hero-metrics{
    display:grid;grid-template-columns:1fr 1fr 1fr;gap:0;
    width:100%;margin-top:12px;border-top:1.5px solid #ede7e0;padding-top:10px;
}
.hm{text-align:center;padding:0 8px;border-right:1.5px solid #ede7e0}
.hm:last-child{border-right:none}
.hm-val{font-family:'Fredoka One',cursive;font-size:1.3rem;line-height:1}
.hm-lbl{font-size:.6rem;font-weight:700;color:#96857a;text-transform:uppercase;letter-spacing:1.2px;margin-top:2px}

/* ── Cards ── */
.card{background:#fff;border-radius:18px;padding:13px 14px;border:2.5px solid #d9cfc7}
.card-blue {border-color:#7ab3c8}
.card-sage {border-color:#8fa882}
.card-coral{border-color:#e8907a}
.card-lbl{font-size:.65rem;font-weight:700;color:#96857a;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:8px}

/* grid */
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:10px}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:10px}

/* temp */
.gauge-wrap{display:flex;justify-content:center}
.temp-big{font-family:'Fredoka One',cursive;font-size:1.45rem;text-align:center;color:#2d2016}
.temp-range{font-size:.62rem;color:#96857a;font-weight:600;text-align:center;line-height:1.6;margin-top:2px}
.hist-btn{
    display:block;margin:7px auto 0;background:#f5f0eb;
    border:2px solid #7ab3c8;border-radius:20px;padding:4px 14px;
    font-family:'Nunito',sans-serif;font-size:.72rem;font-weight:700;color:#7ab3c8;cursor:pointer;
}

/* hum */
.hum-val-big{font-family:'Fredoka One',cursive;font-size:1.45rem;color:#7ab3c8;text-align:center}
.hum-track{background:#e2eff5;border-radius:20px;height:10px;overflow:hidden;margin-top:6px}
.hum-fill {height:100%;border-radius:20px;transition:width .8s,background .5s;background:#7ab3c8}
.drops-row{display:flex;justify-content:center;gap:5px;margin-bottom:4px}
@keyframes db{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
.d1{animation:db 1.8s ease-in-out infinite}
.d2{animation:db 1.8s ease-in-out infinite .3s}
.d3{animation:db 1.8s ease-in-out infinite .6s}

/* alerts */
.alert-item{display:flex;align-items:flex-start;gap:7px;padding:5px 0;
    border-bottom:1px solid #f2ece6;font-size:.71rem;font-weight:600;color:#4a3828;line-height:1.4}
.alert-item:last-child{border-bottom:none}
.ai{width:18px;height:18px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.65rem;flex-shrink:0}
.ai.red{background:#fde4e4;color:#7a1e1e}
.ai.grn{background:#d4ece2;color:#1a6b4a}
.ai.amb{background:#faeeda;color:#633806}

/* readings / records */
.rrow{display:flex;justify-content:space-between;align-items:center;padding:4px 0;
    border-bottom:1px solid #f2ece6;font-size:.73rem}
.rrow:last-child{border-bottom:none}
.rt{color:#96857a;font-weight:600;font-size:.65rem}
.rv{font-weight:700;color:#2d2016}
.recrow{display:flex;align-items:flex-start;gap:7px;padding:5px 0;border-bottom:1px solid #f2ece6}
.recrow:last-child{border-bottom:none}
.ri{width:20px;height:20px;border-radius:50%;background:#e8f4fa;
    display:flex;align-items:center;justify-content:center;font-size:.64rem;flex-shrink:0;margin-top:1px}
.rc{font-size:.71rem;font-weight:600;color:#4a3828;line-height:1.3}
.rc span{font-size:.63rem;color:#96857a}
.dev-box{margin-top:8px;background:#f5f0eb;border-radius:8px;padding:5px 8px}
.dev-id{font-size:.6rem;color:#96857a;font-weight:700;letter-spacing:1px}
.dev-val{font-size:.68rem;font-weight:700;color:#e8907a;font-family:'Courier New',monospace}

/* modal */
.modal-bg{display:none;position:fixed;inset:0;background:rgba(45,32,22,.38);z-index:9999;
    align-items:center;justify-content:center}
.modal-bg.open{display:flex}
.modal{background:#fff;border-radius:22px;border:3px solid #e8907a;padding:22px;
    width:300px;max-width:95vw;position:relative}
.modal-title{font-family:'Fredoka One',cursive;font-size:1.2rem;color:#2d2016;margin-bottom:14px;text-align:center}
.fr{margin-bottom:10px}
.fr label{display:block;font-size:.68rem;font-weight:700;color:#96857a;
    text-transform:uppercase;letter-spacing:1px;margin-bottom:3px}
.fr input{width:100%;border:2px solid #ddd4cc;border-radius:10px;padding:7px 10px;
    font-family:'Nunito',sans-serif;font-size:.86rem;color:#2d2016;outline:none;transition:border .2s}
.fr input:focus{border-color:#e8907a}
.fg{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.mbtns{display:flex;gap:8px;margin-top:14px}
.bsave{flex:1;background:#e8907a;color:#fff;border:none;border-radius:20px;padding:8px;
    font-family:'Fredoka One',cursive;font-size:.9rem;cursor:pointer;letter-spacing:1px}
.bsave:hover{filter:brightness(1.08)}
.bcancel{flex:1;background:#f5f0eb;color:#2d2016;border:2px solid #d9cfc7;border-radius:20px;padding:8px;
    font-family:'Fredoka One',cursive;font-size:.9rem;cursor:pointer}
.bcancel:hover{background:#ede7e0}
.cx{position:absolute;top:10px;right:12px;background:none;border:none;
    font-size:1.1rem;cursor:pointer;color:#e8907a;font-weight:700}
.hlist{max-height:200px;overflow-y:auto;margin-top:8px}
.hi{display:flex;justify-content:space-between;padding:6px 0;
    border-bottom:1px solid #f2ece6;font-size:.75rem;font-weight:600;color:#4a3828}
.hi:last-child{border-bottom:none}
.hi-t{color:#96857a;font-size:.65rem}
.his{font-size:.65rem;padding:2px 7px;border-radius:10px}
.his.s{background:#d4ece2;color:#1a6b4a}
.his.w{background:#fde4e4;color:#7a1e1e}

/* baby anims */
@keyframes breathe{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-7px) scale(1.025)}}
@keyframes blink{0%,85%,100%{transform:scaleY(1)}92%{transform:scaleY(.05)}}
@keyframes wag{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(8deg)}}
@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-4px)}
    40%{transform:translateX(4px)}60%{transform:translateX(-3px)}80%{transform:translateX(3px)}}
@keyframes tearfall{0%{transform:translateY(0);opacity:1}100%{transform:translateY(30px);opacity:0}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SVG Assets
# ─────────────────────────────────────────────────────────────────────────────
LOGO_SVG = """
<svg viewBox="0 0 210 84" height="46" xmlns="http://www.w3.org/2000/svg">
  <!-- B azul -->
  <rect x="2" y="4" width="54" height="76" rx="11" fill="#7ab3c8"/>
  <rect x="14" y="13" width="27" height="26" rx="8" fill="#2d2016" opacity=".84"/>
  <rect x="14" y="45" width="29" height="26" rx="8" fill="#2d2016" opacity=".84"/>
  <!-- cara bebé dentro de B -->
  <circle cx="31" cy="55" r="17" fill="#fce8d8"/>
  <ellipse cx="22" cy="55" rx="3.5" ry="4.5" fill="#fce8d8" stroke="#c8826a" stroke-width=".9"/>
  <ellipse cx="40" cy="55" rx="3.5" ry="4.5" fill="#fce8d8" stroke="#c8826a" stroke-width=".9"/>
  <ellipse cx="27" cy="53" rx="2.2" ry="2.8" fill="#2d2016"/>
  <ellipse cx="35" cy="53" rx="2.2" ry="2.8" fill="#2d2016"/>
  <ellipse cx="25" cy="57" rx="3.5" ry="2.2" fill="#f4a0a0" opacity=".55"/>
  <ellipse cx="37" cy="57" rx="3.5" ry="2.2" fill="#f4a0a0" opacity=".55"/>
  <path d="M27 61 Q31 65 35 61" fill="none" stroke="#2d2016" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M28 39 Q26 32 31 31 Q36 30 36 36 Q36 40 32 40" fill="none" stroke="#c8826a" stroke-width="2" stroke-linecap="round"/>
  <!-- a sage -->
  <rect x="64" y="28" width="52" height="52" rx="13" fill="#8fa882"/>
  <rect x="77" y="39" width="26" height="31" rx="8" fill="#2d2016" opacity=".82"/>
  <!-- e coral -->
  <rect x="124" y="28" width="52" height="52" rx="13" fill="#e8907a"/>
  <rect x="137" y="39" width="26" height="29" rx="8" fill="#2d2016" opacity=".82"/>
  <rect x="124" y="51" width="34" height="13" rx="5" fill="#e8907a"/>
</svg>"""

AVATAR_SVG = """
<svg width="24" height="24" viewBox="0 0 24 24">
  <circle cx="12" cy="10" r="7" fill="#fce8d8" stroke="#e8907a" stroke-width="1.4"/>
  <ellipse cx="8.5" cy="10" rx="2" ry="2.5" fill="#fce8d8" stroke="#e8907a" stroke-width=".8"/>
  <ellipse cx="15.5" cy="10" rx="2" ry="2.5" fill="#fce8d8" stroke="#e8907a" stroke-width=".8"/>
  <ellipse cx="9.5" cy="9.5" rx="1.3" ry="1.6" fill="#2d2016"/>
  <ellipse cx="14.5" cy="9.5" rx="1.3" ry="1.6" fill="#2d2016"/>
  <ellipse cx="7.5" cy="12" rx="2" ry="1.3" fill="#f4a0a0" opacity=".5"/>
  <ellipse cx="16.5" cy="12" rx="2" ry="1.3" fill="#f4a0a0" opacity=".5"/>
  <path d="M10 13.5 Q12 16 14 13.5" fill="none" stroke="#2d2016" stroke-width="1.3" stroke-linecap="round"/>
  <path d="M10.5 5 Q10 2 12 1.5 Q14 1 14 3.5 Q14 5.5 12 5.5" fill="none" stroke="#c8826a" stroke-width="1.2" stroke-linecap="round"/>
</svg>"""

BABY_HAPPY = """
<svg width="130" height="145" viewBox="0 0 130 145" xmlns="http://www.w3.org/2000/svg">
<style>
.hb{transform-origin:65px 95px;animation:breathe 2.6s ease-in-out infinite}
.el{transform-origin:50px 65px;animation:blink 4s ease-in-out infinite}
.er{transform-origin:80px 65px;animation:blink 4s ease-in-out infinite .2s}
.hc{transform-origin:65px 28px;animation:wag 3s ease-in-out infinite}
</style>
<ellipse cx="65" cy="80" rx="56" ry="64" fill="#7ab3c8" opacity=".2"/>
<g class="hb">
  <path d="M44 100 Q65 118 86 100 L88 124 Q65 138 42 124 Z"
    fill="#f8f5f0" stroke="#e8907a" stroke-width="2" stroke-linejoin="round"/>
  <circle cx="65" cy="115" r="4" fill="none" stroke="#e8907a" stroke-width="1.6"/>
  <ellipse cx="65" cy="96" rx="24" ry="13" fill="#fce8d8" stroke="#e8907a" stroke-width="1.8"/>
  <ellipse cx="26" cy="63" rx="7" ry="9" fill="#fce8d8" stroke="#e8907a" stroke-width="1.8"/>
  <ellipse cx="104" cy="63" rx="7" ry="9" fill="#fce8d8" stroke="#e8907a" stroke-width="1.8"/>
  <circle cx="65" cy="55" r="33" fill="#fce8d8" stroke="#e8907a" stroke-width="2"/>
  <g class="hc">
    <path d="M59 26 Q57 17 65 15 Q73 13 73 22 Q73 28 67 28"
      fill="none" stroke="#c8826a" stroke-width="2.2" stroke-linecap="round"/>
  </g>
  <g class="el"><path d="M43 63 Q50 56 57 63" fill="none" stroke="#2d2016" stroke-width="2.4" stroke-linecap="round"/></g>
  <g class="er"><path d="M73 63 Q80 56 87 63" fill="none" stroke="#2d2016" stroke-width="2.4" stroke-linecap="round"/></g>
  <ellipse cx="43" cy="71" rx="8" ry="5" fill="#f4a0a0" opacity=".52"/>
  <ellipse cx="87" cy="71" rx="8" ry="5" fill="#f4a0a0" opacity=".52"/>
  <path d="M53 78 Q65 89 77 78" fill="none" stroke="#2d2016" stroke-width="2.2" stroke-linecap="round"/>
</g></svg>"""

BABY_CRY = """
<svg width="130" height="145" viewBox="0 0 130 145" xmlns="http://www.w3.org/2000/svg">
<style>
.cb{transform-origin:65px 90px;animation:shake .45s ease-in-out infinite}
.tl{animation:tearfall 1s ease-in infinite}
.tr{animation:tearfall 1s ease-in infinite .4s}
</style>
<ellipse cx="65" cy="80" rx="56" ry="64" fill="#e8907a" opacity=".18"/>
<g class="cb">
  <path d="M44 100 Q65 118 86 100 L88 124 Q65 138 42 124 Z"
    fill="#f8f5f0" stroke="#e8907a" stroke-width="2" stroke-linejoin="round"/>
  <circle cx="65" cy="115" r="4" fill="none" stroke="#e8907a" stroke-width="1.6"/>
  <ellipse cx="65" cy="96" rx="24" ry="13" fill="#fce8d8" stroke="#e8907a" stroke-width="1.8"/>
  <ellipse cx="26" cy="63" rx="7" ry="9" fill="#fce8d8" stroke="#e8907a" stroke-width="1.8"/>
  <ellipse cx="104" cy="63" rx="7" ry="9" fill="#fce8d8" stroke="#e8907a" stroke-width="1.8"/>
  <circle cx="65" cy="55" r="33" fill="#fce8d8" stroke="#e8907a" stroke-width="2"/>
  <path d="M59 26 Q57 17 65 15 Q73 13 73 22 Q73 28 67 28"
    fill="none" stroke="#c8826a" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M40 49 Q49 43 57 49" fill="none" stroke="#2d2016" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M73 49 Q81 43 90 49" fill="none" stroke="#2d2016" stroke-width="1.8" stroke-linecap="round"/>
  <ellipse cx="50" cy="62" rx="5" ry="6" fill="#2d2016"/>
  <ellipse cx="80" cy="62" rx="5" ry="6" fill="#2d2016"/>
  <ellipse cx="48" cy="59" rx="1.5" ry="2" fill="white"/>
  <ellipse cx="78" cy="59" rx="1.5" ry="2" fill="white"/>
  <ellipse cx="42" cy="71" rx="9" ry="6" fill="#e87070" opacity=".42"/>
  <ellipse cx="88" cy="71" rx="9" ry="6" fill="#e87070" opacity=".42"/>
  <path d="M53 80 Q65 73 77 80" fill="none" stroke="#2d2016" stroke-width="2.2" stroke-linecap="round"/>
  <g class="tl"><path d="M46 68 Q44 76 46 83" fill="none" stroke="#7ab3c8" stroke-width="2.2" stroke-linecap="round"/></g>
  <g class="tr"><path d="M84 68 Q86 76 84 83" fill="none" stroke="#7ab3c8" stroke-width="2.2" stroke-linecap="round"/></g>
  <ellipse cx="55" cy="127" rx="4" ry="5" fill="#7ab3c8" opacity=".38"/>
  <ellipse cx="65" cy="131" rx="3.5" ry="4.5" fill="#7ab3c8" opacity=".3"/>
  <ellipse cx="75" cy="127" rx="4" ry="5" fill="#7ab3c8" opacity=".35"/>
</g></svg>"""

# ─────────────────────────────────────────────────────────────────────────────
#  Sidebar config
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuración BAE")
    hum_threshold = st.slider("💧 Umbral humedad (%)", 40, 90, 65)
    temp_max      = st.slider("🌡️ Temperatura máx (°C)", 32, 40, 37)
    temp_min      = st.slider("❄️ Temperatura mín (°C)", 20, 30, 36)
    st.markdown("---")
    st.caption("🌿 PCB biodegradable · Sensor orgánico\nCarcasa bambú · Tinta vegetal")
    demo_mode = st.toggle("🎮 Modo demostración", value=True)

# ─────────────────────────────────────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────────────────────────────────────
if "history"  not in st.session_state: st.session_state.history  = []
if "last_log" not in st.session_state: st.session_state.last_log = datetime.now()
if "last_alt" not in st.session_state: st.session_state.last_alt = None
if "profile"  not in st.session_state:
    st.session_state.profile = dict(name="Emma", age="6 meses",
                                    weight=7.2, height=65,
                                    bdate="2024-09-15", notes="")

# ─────────────────────────────────────────────────────────────────────────────
#  Sensor values
# ─────────────────────────────────────────────────────────────────────────────
if demo_mode:
    t    = time.time()
    hum  = round(45 + 23 * abs(math.sin(t / 19)), 1)
    temp = round(36.5 + 0.8 * math.sin(t / 28) + random.uniform(-0.2, 0.2), 1)
else:
    hum  = st.sidebar.slider("💧 Humedad (%)",       0,    100, 45)
    temp = st.sidebar.slider("🌡️ Temperatura (°C)", 18.0, 42.0, 36.5, 0.1)

wet        = hum  > hum_threshold
temp_alert = temp > temp_max or temp < temp_min

# Log every 5 s
now = datetime.now()
if (now - st.session_state.last_log).seconds >= 5:
    st.session_state.history.insert(0, {
        "time": now.strftime("%H:%M"),
        "date": now.strftime("%d %b"),
        "temp": temp, "hum": hum, "wet": wet,
    })
    st.session_state.history = st.session_state.history[:100]
    st.session_state.last_log = now
    if temp > temp_max:
        st.session_state.last_alt = temp

p    = st.session_state.profile
hist = st.session_state.history

# ─────────────────────────────────────────────────────────────────────────────
#  Derived display values
# ─────────────────────────────────────────────────────────────────────────────
pill_cls  = "spill alert" if (wet or temp_alert) else "spill"
pill_txt  = ("Pañal mojado" if wet else "Temperatura elevada") if (wet or temp_alert) else "Todo estable"

hero_lbl  = "¡Pañal mojado! 💦" if wet else "Bebé estable ✓"
hero_sub  = "Cambiar pañal ahora" if wet else "Pañal seco — todo en orden"
hero_lc   = "#a03020" if wet else "#2d5a3d"
hero_sc   = "#e8907a" if wet else "#8fa882"

hm_tc     = "#e8907a" if temp > temp_max else ("#7ab3c8" if temp < temp_min else "#7ab3c8")
hm_hc     = "#e8907a" if wet else "#7ab3c8"
hm_sc     = "#e8907a" if wet else "#8fa882"
hm_sl     = "ALERTA"  if wet else "NORMAL"

gauge_pct = max(0.0, min(1.0, (temp - 35) / 5))
gauge_off = round(113 - gauge_pct * 113, 1)
gauge_col = "#8fa882" if temp < 36 else ("#7ab3c8" if temp <= 37.5 else "#e8907a")
gauge_cx  = round(48 + 36 * math.cos(math.pi + gauge_pct * math.pi), 1)
gauge_cy  = round(52 + 36 * math.sin(math.pi + gauge_pct * math.pi), 1)

hum_pct   = min(hum / 100.0, 1.0)
hum_col   = "#e8907a" if wet else "#7ab3c8"
drop_col  = "#e8907a" if wet else "#7ab3c8"

last_alt_txt = f"Última alerta: {st.session_state.last_alt}°C" if st.session_state.last_alt else "Sin alertas recientes"

# Alerts list
alerts_html = ""
if temp > temp_max:
    alerts_html += f'<div class="alert-item"><div class="ai red">!</div><div>Temperatura elevada: {temp}°C</div></div>'
if temp < temp_min:
    alerts_html += f'<div class="alert-item"><div class="ai amb">!</div><div>Temperatura baja: {temp}°C</div></div>'
if wet:
    alerts_html += f'<div class="alert-item"><div class="ai red">!</div><div>Pañal mojado — cambiar ahora</div></div>'
if not alerts_html:
    alerts_html = '<div class="alert-item"><div class="ai grn">✓</div><div style="color:#1a6b4a">Sin alertas — todo bien</div></div>'

# Readings list
readings_html = "".join(
    f'<div class="rrow"><span class="rt">{e["time"]}</span>'
    f'<span class="rv" style="color:{"#e8907a" if e["temp"]>temp_max else "#2d2016"}">{e["temp"]}°C</span></div>'
    for e in hist[:4]
) or '<div style="font-size:.74rem;color:#96857a;padding:6px 0">Esperando lecturas...</div>'

# Sparkline
spark_html = ""
if len(hist) >= 2:
    vals = [e["temp"] for e in hist[:14]][::-1]
    mn, mx = min(vals), max(vals)
    rng = mx - mn or 1
    pts = " ".join(
        f"{round(3 + i*(194)/(len(vals)-1), 1)},{round(27 - (v-mn)/rng*24, 1)}"
        for i, v in enumerate(vals)
    )
    spark_html = f'<svg width="100%" height="30" viewBox="0 0 200 30" preserveAspectRatio="none" style="margin-top:6px"><polyline points="{pts}" fill="none" stroke="#7ab3c8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# Records list
records_html = "".join(
    f'<div class="recrow"><div class="ri">🕐</div>'
    f'<div class="rc">{e["date"]} · {e["time"]}'
    f'<br><span>{e["temp"]}°C · {e["hum"]}% · {"Mojado" if e["wet"] else "Seco"}</span></div></div>'
    for e in hist[:2]
) or '<div style="font-size:.74rem;color:#96857a;padding:6px 0">Sin registros aún...</div>'

# History modal rows
hist_rows = "".join(
    f'<div class="hi"><div><div>{e["date"]} {e["time"]}</div>'
    f'<div class="hi-t">{e["temp"]}°C · {e["hum"]}%</div></div>'
    f'<span class="his {"w" if e["wet"] else "s"}">{"Mojado" if e["wet"] else "Seco"}</span></div>'
    for e in hist[:30]
) or '<div style="text-align:center;color:#96857a;padding:16px;font-size:.8rem">Sin registros aún</div>'

# ─────────────────────────────────────────────────────────────────────────────
#  RENDER
# ─────────────────────────────────────────────────────────────────────────────
baby_svg = BABY_CRY if wet else BABY_HAPPY

st.markdown(f"""
<!-- ── TOPBAR ── -->
<div class="topbar">
  <div>{LOGO_SVG}</div>
  <div style="display:flex;align-items:center;gap:8px">
    <div class="{pill_cls}"><div class="sdot"></div><span>{pill_txt}</span></div>
    <div class="baby-profile" onclick="document.getElementById('emod').classList.add('open')">
      <div class="avatar-sm">{AVATAR_SVG}</div>
      <div>
        <div class="baby-name" id="dn">{p['name']}</div>
        <div class="baby-age">{p['age']}</div>
      </div>
    </div>
  </div>
</div>

<!-- ── HERO ── -->
<div class="hero">
  <div style="position:relative;z-index:1">{baby_svg}</div>
  <div class="hero-lbl" style="color:{hero_lc}">{hero_lbl}</div>
  <div class="hero-sub" style="color:{hero_sc}">{hero_sub}</div>
  <div class="hero-metrics">
    <div class="hm">
      <div class="hm-val" style="color:{hm_tc}">{temp}°C</div>
      <div class="hm-lbl">Temperatura</div>
    </div>
    <div class="hm">
      <div class="hm-val" style="color:{hm_hc}">{hum}%</div>
      <div class="hm-lbl">Humedad</div>
    </div>
    <div class="hm">
      <div class="hm-val" style="color:{hm_sc};font-size:.9rem;padding-top:4px">{hm_sl}</div>
      <div class="hm-lbl">Estado</div>
    </div>
  </div>
</div>

<!-- ── GRID 3 ── -->
<div class="g3">

  <!-- Temperatura -->
  <div class="card card-blue">
    <div class="card-lbl">Temperatura</div>
    <div class="gauge-wrap">
      <svg width="96" height="56" viewBox="0 0 96 56">
        <path d="M8 52 A36 36 0 0 1 88 52" fill="none" stroke="#e2eff5" stroke-width="9" stroke-linecap="round"/>
        <path d="M8 52 A36 36 0 0 1 88 52" fill="none" stroke="{gauge_col}" stroke-width="9"
          stroke-linecap="round" stroke-dasharray="113" stroke-dashoffset="{gauge_off}"/>
        <circle cx="{gauge_cx}" cy="{gauge_cy}" r="5" fill="{gauge_col}"/>
      </svg>
    </div>
    <div class="temp-big">{temp}°C</div>
    <div class="temp-range">Normal 36.0–37.5°C<br>
      <span style="color:#e8907a">{last_alt_txt}</span>
    </div>
    <button class="hist-btn" onclick="document.getElementById('hmod').classList.add('open')">Ver historial</button>
  </div>

  <!-- Humedad -->
  <div class="card card-blue">
    <div class="card-lbl">Humedad pañal</div>
    <div class="drops-row">
      <svg class="d1" width="22" height="30" viewBox="0 0 28 38"><path d="M14 2 Q24 16 24 24 A10 10 0 0 1 4 24 Q4 16 14 2Z" fill="{drop_col}"/></svg>
      <svg class="d2" width="17" height="23" viewBox="0 0 28 38"><path d="M14 2 Q24 16 24 24 A10 10 0 0 1 4 24 Q4 16 14 2Z" fill="{drop_col}" opacity=".65"/></svg>
      <svg class="d3" width="12" height="16" viewBox="0 0 28 38"><path d="M14 2 Q24 16 24 24 A10 10 0 0 1 4 24 Q4 16 14 2Z" fill="{drop_col}" opacity=".4"/></svg>
    </div>
    <div class="hum-val-big" style="color:{hum_col}">{hum}%</div>
    <div class="hum-track"><div class="hum-fill" style="width:{hum_pct*100:.0f}%;background:{hum_col}"></div></div>
    <div style="display:flex;justify-content:space-between;font-size:.58rem;font-weight:700;color:#96857a;margin-top:4px">
      <span>0%</span><span>{hum_threshold}%</span><span>100%</span>
    </div>
  </div>

  <!-- Alertas -->
  <div class="card card-coral">
    <div class="card-lbl">Alertas</div>
    {alerts_html}
  </div>

</div>

<!-- ── GRID 2 ── -->
<div class="g2">

  <div class="card card-sage">
    <div class="card-lbl">Últimas lecturas</div>
    {readings_html}
    {spark_html}
  </div>

  <div class="card card-sage">
    <div class="card-lbl">Último registro</div>
    {records_html}
    <div class="dev-box">
      <div class="dev-id">ID DISPOSITIVO</div>
      <div class="dev-val">0x1234...5def</div>
    </div>
  </div>

</div>

<!-- ── MODAL PERFIL ── -->
<div class="modal-bg" id="emod">
  <div class="modal">
    <button class="cx" onclick="document.getElementById('emod').classList.remove('open')">✕</button>
    <div class="modal-title">✏️ Perfil del bebé</div>
    <form method="get" action="">
      <div class="fr"><label>Nombre</label>
        <input name="pname" type="text" value="{p['name']}" placeholder="Nombre"></div>
      <div class="fg">
        <div class="fr"><label>Edad</label>
          <input name="page" type="text" value="{p['age']}" placeholder="6 meses"></div>
        <div class="fr"><label>Peso (kg)</label>
          <input name="pweight" type="number" step="0.1" value="{p['weight']}" placeholder="7.2"></div>
      </div>
      <div class="fg">
        <div class="fr"><label>Talla (cm)</label>
          <input name="pheight" type="number" step="0.5" value="{p['height']}" placeholder="65"></div>
        <div class="fr"><label>Fecha nac.</label>
          <input name="pbdate" type="date" value="{p['bdate']}"></div>
      </div>
      <div class="fr"><label>Notas médicas</label>
        <input name="pnotes" type="text" value="{p['notes']}" placeholder="Alergias, medicamentos..."></div>
      <div class="mbtns">
        <button type="button" class="bcancel" onclick="document.getElementById('emod').classList.remove('open')">Cancelar</button>
        <button type="submit" class="bsave">Guardar ✓</button>
      </div>
    </form>
  </div>
</div>

<!-- ── MODAL HISTORIAL ── -->
<div class="modal-bg" id="hmod">
  <div class="modal">
    <button class="cx" onclick="document.getElementById('hmod').classList.remove('open')">✕</button>
    <div class="modal-title">📋 Historial</div>
    <div class="hlist">{hist_rows}</div>
    <div class="mbtns" style="margin-top:12px">
      <button class="bcancel" onclick="document.getElementById('hmod').classList.remove('open')">Cerrar</button>
    </div>
  </div>
</div>

<script>
document.querySelectorAll('.modal-bg').forEach(b=>
  b.addEventListener('click',e=>{{if(e.target===b)b.classList.remove('open')}})
);
</script>
""", unsafe_allow_html=True)

# ── Handle profile form submission ──────────────────────────────────────────
params = st.query_params
if "pname" in params:
    st.session_state.profile["name"]   = params.get("pname",   p["name"])
    st.session_state.profile["age"]    = params.get("page",    p["age"])
    st.session_state.profile["weight"] = params.get("pweight", p["weight"])
    st.session_state.profile["height"] = params.get("pheight", p["height"])
    st.session_state.profile["bdate"]  = params.get("pbdate",  p["bdate"])
    st.session_state.profile["notes"]  = params.get("pnotes",  "")
    st.query_params.clear()
    st.rerun()

# Auto-refresh in demo mode
if demo_mode:
    time.sleep(3)
    st.rerun()
