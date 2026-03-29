import streamlit as st
from streamlit_option_menu import option_menu
from enviar_mail import enviar_m, enviar_cancelacion, avisar_nuevo_turno, avisar_cancelacion
from google_sheets import GoogleSheets
#from enviar_wsp import enviar_whatsapp
import re
import uuid
from google_calendar import GoogleCalendar
import numpy as np
import datetime as dt

# ── Variables ──────────────────────────────────────────────────────────────────
page_title = "DePelos · Reservas"
page_icon = "✂"
layout = "centered"

horarios = ["10:00","11:00","12:00","13:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00"]
servicios = ["Corte — $10.000", "Corte + Barba — $12.000", "Tintura — $30.000", "Alisado — $30.000"]
empleados = ["Maxi Ruiz"]

documento   = "gestión-app-reservas"
sheet = "reservas"
credenciales = st.secrets["google"]["credenciales_google"]
idCalendar = "lucasruiiz912@gmail.com"

timeZone = "America/Argentina/Cordoba"

# ── CSS ────────────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
/* ─── Google Fonts ─── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Mono:wght@300;400;500&display=swap');

/* ─── Root palette ─── */
:root {
    --bg:          #0d0d0d;
    --bg-card:     #141414;
    --bg-input:    #1a1a1a;
    --border:      #2e2e2e;
    --border-hot:  #c9a84c;
    --gold:        #c9a84c;
    --gold-dim:    #8a6e2f;
    --cream:       #f0e6cc;
    --muted:       #666;
    --text:        #e8dcc8;
    --danger:      #b84040;
    --success:     #3a7a4e;
    --radius:      4px;
}

/* ─── Global ─── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ─── Hide default Streamlit decoration ─── */
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 2px; }

/* ─── Hero banner ─── */
.hero-wrap {
    border: 1px solid var(--border);
    border-top: 3px solid var(--gold);
    background: var(--bg-card);
    padding: 2.5rem 2rem 2rem;
    margin-bottom: 0.25rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: "";
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 39px,
        rgba(201,168,76,.04) 39px,
        rgba(201,168,76,.04) 40px
    );
    pointer-events: none;
}
.hero-scissors {
    font-size: 2.2rem;
    display: block;
    margin-bottom: 0.5rem;
    opacity: .85;
}
.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.8rem !important;
    font-weight: 900 !important;
    color: var(--gold) !important;
    letter-spacing: .08em;
    margin: 0 0 0.2rem !important;
    line-height: 1.1;
    text-transform: uppercase;
}
.hero-sub {
    font-size: .72rem;
    letter-spacing: .35em;
    color: var(--muted);
    text-transform: uppercase;
    margin: 0;
}
.hero-rule {
    width: 60px; height: 1px;
    background: var(--gold);
    margin: 1rem auto 0;
    opacity: .5;
}

/* ─── Option menu override ─── */
[data-testid="stHorizontalBlock"] nav,
.stOptionMenu > div { background: transparent !important; }

ul[data-testid="stHorizontalBlock"] {
    border-bottom: 1px solid var(--border) !important;
}

/* ─── Section headers ─── */
.section-label {
    font-size: .65rem;
    letter-spacing: .3em;
    text-transform: uppercase;
    color: var(--gold-dim);
    margin: 1.8rem 0 .8rem;
    display: flex;
    align-items: center;
    gap: .6rem;
}
.section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ─── Inputs ─── */
input, textarea, select,
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div,
[data-baseweb="select"] > div {
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: .82rem !important;
}

input:focus, textarea:focus,
[data-baseweb="input"]:focus-within > div,
[data-baseweb="textarea"]:focus-within > div,
[data-baseweb="select"]:focus-within > div {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,.15) !important;
}

/* ─── Labels ─── */
label[data-testid="stWidgetLabel"] p,
.stTextInput label, .stTextArea label,
.stSelectbox label, .stDateInput label {
    font-size: .65rem !important;
    letter-spacing: .15em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    font-family: 'DM Mono', monospace !important;
    font-weight: 500 !important;
}

/* ─── Date input ─── */
[data-baseweb="base-input"] {
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
}

/* ─── Button ─── */
.stButton > button {
    width: 100%;
    padding: .75rem 2rem;
    background: transparent !important;
    border: 1px solid var(--gold) !important;
    border-radius: var(--radius) !important;
    color: var(--gold) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: .72rem !important;
    letter-spacing: .35em !important;
    text-transform: uppercase !important;
    cursor: pointer;
    transition: all .2s ease;
    margin-top: 1rem;
}
.stButton > button:hover {
    background: var(--gold) !important;
    color: var(--bg) !important;
}

/* ─── Alerts ─── */
[data-testid="stAlert"] {
    background: var(--bg-card) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: .8rem !important;
}
[data-testid="stAlert"][data-type="error"],
div[role="alert"][class*="error"] {
    border-left: 3px solid var(--danger) !important;
}
[data-testid="stAlert"][data-type="success"],
div[role="alert"][class*="success"] {
    border-left: 3px solid var(--success) !important;
}

/* ─── Info grid (Información tab) ─── */
.info-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    margin-bottom: .75rem;
}
.info-card-title {
    font-size: .6rem;
    letter-spacing: .3em;
    text-transform: uppercase;
    color: var(--gold-dim);
    margin-bottom: .6rem;
}
.schedule-row {
    display: flex;
    justify-content: space-between;
    padding: .28rem 0;
    border-bottom: 1px solid var(--border);
    font-size: .78rem;
}
.schedule-row:last-child { border-bottom: none; }
.schedule-day { color: var(--muted); }
.schedule-time { color: var(--text); font-variant-numeric: tabular-nums; }

/* ─── Map iframe ─── */
iframe {
    border-radius: var(--radius) !important;
    filter: grayscale(1) contrast(1.1) !important;
    opacity: .85;
}

/* ─── Spinner ─── */
[data-testid="stSpinner"] { color: var(--gold) !important; }

/* ─── Dividers ─── */
hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}

/* ─── Selectbox popup ─── */
[data-baseweb="popover"] ul {
    background: #1a1a1a !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}
[data-baseweb="popover"] li {
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: .8rem !important;
}
[data-baseweb="popover"] li:hover {
    background: #252525 !important;
}
</style>
"""

# ── Funciones ────────────────────────────────────────────────────────────────────
def validate_email(email):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

def generate_uid():
    return str(uuid.uuid4())[:8].upper()

def sumar_hora(tiempo):
    parsed_tiempo = dt.datetime.strptime(tiempo,"%H:%M").time()
    nuevo_t = (dt.datetime.combine(dt.date.today(), parsed_tiempo) + dt.timedelta(hours=1, minutes=00)).time()
    return nuevo_t.strftime("%H:%M")

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <span class="hero-scissors">✂</span>
    <h1 class="hero-title">De Pelos</h1>
    <p class="hero-sub">Peluquería &amp; Barbería · Reservá tu turno</p>
    <div class="hero-rule"></div>
</div>
""", unsafe_allow_html=True)

# ── Nav ────────────────────────────────────────────────────────────────────────
selected = option_menu(
    menu_title=None,
    options=["Reservar", "Cancelar", "Información"],
    icons=["calendar-check", "calendar-x", "info-circle"],
    orientation="horizontal",
    styles={
        "container":     {"background-color": "#141414", "border": "1px solid #2e2e2e",
                          "border-top": "none", "padding": "0 !important"},
        "icon":          {"color": "#666", "font-size": "13px"},
        "nav-link":      {"font-family": "'DM Mono', monospace", "font-size": "0.68rem",
                          "letter-spacing": "0.25em", "text-transform": "uppercase",
                          "color": "#666", "padding": "0.9rem 1.5rem",
                          "--hover-color": "#1e1e1e"},
        "nav-link-selected": {"background-color": "#1e1e1e", "color": "#c9a84c",
                              "border-bottom": "2px solid #c9a84c"},
    }
)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB: INFORMACIÓN
# ═══════════════════════════════════════════════════════════════════════════════
if selected == "Información":
    st.markdown("""
    <div style="height:.5rem"></div>
    <div class="info-card">
        <div class="info-card-title">Horarios de atención</div>
        <div class="schedule-row"><span class="schedule-day">Lunes</span><span class="schedule-time">10:00 – 13:00 · 16:00 – 22:00</span></div>
        <div class="schedule-row"><span class="schedule-day">Martes</span><span class="schedule-time">10:00 – 13:00 · 16:00 – 22:00</span></div>
        <div class="schedule-row"><span class="schedule-day">Miércoles</span><span class="schedule-time">10:00 – 13:00 · 16:00 – 22:00</span></div>
        <div class="schedule-row"><span class="schedule-day">Jueves</span><span class="schedule-time">10:00 – 13:00 · 16:00 – 22:00</span></div>
        <div class="schedule-row"><span class="schedule-day">Viernes</span><span class="schedule-time">10:00 – 13:00 · 16:00 – 22:00</span></div>
        <div class="schedule-row"><span class="schedule-day">Sábados</span><span class="schedule-time">10:00 – 13:00 · 16:00 – 22:00</span></div>
        <div class="schedule-row"><span class="schedule-day">Domingos</span><span class="schedule-time">10:00 – 13:00 · 16:00 – 22:00</span></div>
    </div>
    """, unsafe_allow_html=True)

    col_wsp, col_ig = st.columns(2)
    col_wsp.markdown("""
    <div class="info-card">
        <div class="info-card-title">Celular</div>
        <div style="font-size:.9rem; color:#e8dcc8;">📞 3549-000000</div>
    </div>
    """, unsafe_allow_html=True)
    col_ig.markdown("""
    <div class="info-card">
        <div class="info-card-title">Instagram</div>
        <div style="font-size:.9rem;"><a href="https://www.instagram.com/depelosruiz/" style="color:#c9a84c; text-decoration:none;">@DePelosRuiz ↗</a></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Dónde encontrarnos</div>', unsafe_allow_html=True)
    st.markdown("""
    <iframe src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d6865.649941068577!2d-65.3918415!3d-30.63889!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x942c21bb45f4b1af%3A0xaed5af0102cb132b!2sDe%20Pelos%20peluquer%C3%ADa%20%26%20barberia!5e0!3m2!1ses!2sar!4v1773407301027!5m2!1ses!2sar"
        width="100%" height="380" style="border:0; display:block;" allowfullscreen="" loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"></iframe>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB: RESERVAR
# ═══════════════════════════════════════════════════════════════════════════════
if selected == "Reservar":
    st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Tus datos</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2) # c1, c2, c3_tel = st.columns(3)
    nombre   = c1.text_input("Nombre y apellido *", placeholder="Juan Pérez")
    email    = c2.text_input("Email *", placeholder="juan@email.com")
    # telefono = c3_tel.text_input("WhatsApp *", placeholder="3512345678")

    st.markdown('<div class="section-label">Turno</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    fecha = c3.date_input("Fecha *", min_value=dt.date.today())
    if fecha:
        calendar = GoogleCalendar(credenciales, idCalendar)
        horas_bloqueadas = calendar.get_events_start_time(str(fecha))
        result_horas = np.setdiff1d(horarios, horas_bloqueadas)

         # Filtrar horarios pasados si es hoy
        ahora = dt.datetime.now(dt.timezone(dt.timedelta(hours=-3)))
        if fecha == ahora.date():
            result_horas = [h for h in result_horas if dt.datetime.strptime(h, "%H:%M").time() > ahora.time()]
    if len(result_horas) == 0:
        st.warning("No hay horarios disponibles para este día.")
        hora = None
    else:
        hora = c4.selectbox("Hora *", result_horas)

    st.markdown('<div class="section-label">Servicio</div>', unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    servicio = c5.selectbox("Servicio *", servicios)
    barbero = c6.selectbox("Profesional", empleados)

    st.markdown('<div class="section-label">Notas</div>', unsafe_allow_html=True)
    nota = st.text_area("Detalles opcionales", placeholder="Ej: Llegaré unos minutos tarde · Voy con un acompañantepy",
                        height=90, label_visibility="collapsed")

    enviar = st.button("✦  Confirmar reserva  ✦")

    # ── Backend ──────────────────────────────────────────────────────────────
    if enviar:
        with st.spinner("Afilando tijeras..."):
            if nombre == "" or email == "" or hora is None:
                st.warning("Completá los campos obligatorios marcados con *")
            elif not validate_email(email):
                st.warning("El email ingresado no es válido.")
            else:
                #Crear evento en google calendar
                parsed_tiempo = dt.datetime.strptime(hora, "%H:%M").time()
                horas = parsed_tiempo.hour
                minutos = parsed_tiempo.minute
                end_horas = sumar_hora(hora)
                parsed_tiempo2 = dt.datetime.strptime(end_horas, "%H:%M").time()
                horas2 = parsed_tiempo2.hour
                minutos2 = parsed_tiempo2.minute
                start_time = dt.datetime(fecha.year, fecha.month, fecha.day, horas, minutos).strftime('%Y-%m-%dT%H:%M:%S')
                end_time = dt.datetime(fecha.year, fecha.month, fecha.day, horas2, minutos2).strftime('%Y-%m-%dT%H:%M:%S')
                calendar = GoogleCalendar(credenciales, idCalendar)
                calendar.create_event(nombre, start_time, end_time, timeZone)
                #Crear registro en google sheet
                uid = generate_uid()
                data = [[nombre, email, str(fecha), hora, servicio, barbero, nota, uid]]
                gs = GoogleSheets(credenciales, documento, sheet)
                range = gs.ultimaFilaRango()
                gs.write_data(range, data)
                # if telefono:
                #     enviar_whatsapp(telefono, nombre, fecha, hora, servicio, empleado)
                #Enviar mail de confirmacion al usuario
                enviar_m(email, nombre, fecha, hora, servicio, barbero, nota, uid)
                avisar_nuevo_turno(nombre, fecha, hora, servicio, barbero, nota)

                st.success(f"✓  Turno reservado · {str(fecha)} a las {hora}")
                st.markdown(f"""
                <div style="background:#141414; border:1px solid #2e2e2e; border-left:3px solid #c9a84c;
                     border-radius:4px; padding:1rem 1.25rem; margin-top:.5rem;
                     font-family:'DM Mono',monospace; font-size:.78rem; color:#e8dcc8; line-height:1.8;">
                    <span style="color:#666; font-size:.6rem; letter-spacing:.25em; text-transform:uppercase;">Resumen</span><br>
                    <b style="color:#c9a84c">{nombre}</b><br>
                    {servicio}<br>
                    {str(fecha)} · {hora}<br>
                    {barbero}
                </div>
                """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB: CANCELAR
# ═══════════════════════════════════════════════════════════════════════════════
if selected == "Cancelar":
    st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)
 
    st.markdown('<div class="section-label">Cancelar reserva</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#141414; border:1px solid #2e2e2e; border-left:3px solid #c9a84c;
         border-radius:4px; padding:.9rem 1.2rem; margin-bottom:1.2rem;
         font-family:'DM Mono',monospace; font-size:.76rem; color:#666; line-height:1.7;">
        Ingresá el email y el código único que recibiste en el mail de confirmación.
    </div>
    """, unsafe_allow_html=True)
 
    c_email, c_uuid = st.columns(2)
    cancel_email = c_email.text_input("Email *", placeholder="juan@email.com", key="cancel_email")
    cancel_uuid  = c_uuid.text_input("Código de reserva *", placeholder="xxxxxxxx", key="cancel_uuid")
 
    cancelar = st.button("✦  Cancelar reserva  ✦")
 
    if cancelar:
        with st.spinner("Buscando tu reserva..."):
            if not cancel_email or not cancel_uuid:
                st.warning("Completá los campos obligatorios marcados con *")
            elif not validate_email(cancel_email):
                st.warning("El email ingresado no es válido.")
            else:
                gs = GoogleSheets(credenciales, documento, sheet)
                all_data = gs.read_data()
 
                fila_encontrada = None
                idx_encontrado  = None
 
                for i, fila in enumerate(all_data):
                    if i == 0:
                        continue
                    if len(fila) >= 8 and fila[7].strip().upper() == cancel_uuid.strip().upper() and fila[1].strip().lower() == cancel_email.strip().lower():
                        fila_encontrada = fila
                        idx_encontrado  = i
                        break

                if fila_encontrada is None:
                    st.error("No encontramos una reserva con esos datos. Verificá el email y el código.")
                else:
                    nombre_r   = fila_encontrada[0]
                    email_r    = fila_encontrada[1]
                    fecha_r    = fila_encontrada[2]
                    hora_r     = fila_encontrada[3]
                    servicio_r = fila_encontrada[4]
                    barbero_r  = fila_encontrada[5]
 
                    # Eliminar evento de Google Calendar
                    try:
                        calendar = GoogleCalendar(credenciales, idCalendar)
                        eventos  = calendar.get_events(fecha_r)
                        for evento in eventos:
                            start = evento.get("start", {}).get("dateTime", "")
                            if hora_r in start and nombre_r in evento.get("summary", ""):
                                calendar.delete_event(evento["id"])
                                break
                    except Exception as e:
                        st.warning(f"No se pudo eliminar el evento del calendario: {e}")
 
                    # Borrar fila de Google Sheets
                    fila_num = idx_encontrado + 2
                    try:
                        gs.delete_row(fila_num)
                    except Exception as e:
                        st.warning(f"No se pudo eliminar la reserva de la planilla: {e}")
 
                    # Enviar mail de cancelación
                    try:
                        enviar_cancelacion(email_r, nombre_r, fecha_r, hora_r, servicio_r, barbero_r)
                        avisar_cancelacion(nombre_r, fecha_r, hora_r, servicio_r, barbero_r)
                    except Exception as e:
                        st.warning(f"Error exacto: {type(e).__name__}: {e}")
 
                    st.success(f"✓  Reserva cancelada · {fecha_r} a las {hora_r}")
                    st.markdown(f"""
                    <div style="background:#141414; border:1px solid #2e2e2e; border-left:3px solid #b84040;
                         border-radius:4px; padding:1rem 1.25rem; margin-top:.5rem;
                         font-family:'DM Mono',monospace; font-size:.78rem; color:#e8dcc8; line-height:1.8;">
                        <span style="color:#666; font-size:.6rem; letter-spacing:.25em; text-transform:uppercase;">Reserva cancelada</span><br>
                        <b style="color:#c9a84c">{nombre_r}</b><br>
                        {servicio_r}<br>
                        {fecha_r} · {hora_r}<br>
                        {barbero_r}
                    </div>
                    """, unsafe_allow_html=True)