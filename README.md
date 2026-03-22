# 💈 App de Reservas de Turnos

Aplicación web desarrollada con **Streamlit** para gestionar reservas de turnos de forma simple y automatizada. Pensada originalmente para **peluquerías**, su diseño flexible la hace adaptable a cualquier servicio que requiera gestión de turnos: consultorios médicos, spas, centros de estética, estudios profesionales y más.

---

## ✨ Funcionalidades

- 📋 **Reserva de turnos** — formulario intuitivo para seleccionar fecha, hora y datos del cliente
- 📧 **Notificaciones por email** — confirmación automática al momento de realizar la reserva
- 📆 **Google Calendar** — los turnos se agregan automáticamente al calendario del negocio
- 📊 **Google Sheets** — registro centralizado de todas las reservas en una hoja de cálculo

---

## 🏪 Casos de uso

Si bien la app fue desarrollada para una peluquería, puede adaptarse fácilmente para:

| Servicio | Ejemplo |
|---|---|
| 💇 Peluquería / Estética | Cortes, coloraciones, tratamientos |
| 🏥 Salud | Consultorios médicos, odontología, psicología |
| 💆 Bienestar | Spa, masajes, yoga |
| 🐾 Veterinaria | Consultas, grooming |
| 📚 Educación | Clases particulares, tutorías |

---

## 🛠️ Tecnologías utilizadas

- [Streamlit](https://streamlit.io/) — interfaz web
- [Google Calendar API](https://developers.google.com/calendar) — gestión de eventos
- [gspread](https://gspread.readthedocs.io/) — integración con Google Sheets
- [Twilio](https://www.twilio.com/) — comunicaciones
- Python 3.x

---

## 🚀 Instalación local

1. Cloná el repositorio:
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

2. Creá y activá un entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

3. Instalá las dependencias:
```bash
pip install -r requirements.txt
```

4. Configurá las credenciales (ver sección siguiente)

5. Ejecutá la app:
```bash
streamlit run app.py
```

---

## 🔐 Configuración de credenciales

La app requiere credenciales de Google para funcionar. Creá un archivo `.streamlit/secrets.toml` con el siguiente contenido:

```toml
[gcp_service_account]
type = "service_account"
project_id = "TU_PROJECT_ID"
private_key_id = "TU_KEY_ID"
private_key = "TU_PRIVATE_KEY"
client_email = "TU_CLIENT_EMAIL"
client_id = "TU_CLIENT_ID"

[email]
sender = "TU_EMAIL@gmail.com"
password = "TU_APP_PASSWORD"
```

> ⚠️ **Nunca subas este archivo al repositorio.** Asegurate de que `.streamlit/secrets.toml` esté en tu `.gitignore`.

---

## ☁️ Deploy en Streamlit Cloud

1. Subí el código a GitHub
2. Ingresá a [share.streamlit.io](https://share.streamlit.io)
3. Conectá tu repositorio y seleccioná `app.py` como módulo principal
4. En **Settings → Secrets**, pegá el contenido de tu `secrets.toml`
5. ¡Listo!

---

## 📁 Estructura del proyecto

```
├── app.py                  # Archivo principal
├── google_calendar.py      # Integración con Google Calendar
├── google_sheets.py        # Integración con Google Sheets
├── enviar_mail.py          # Envío de emails
├── requirements.txt        # Dependencias
└── .streamlit/
    └── secrets.toml        # Credenciales (no subir al repo)
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si querés adaptar la app para otro tipo de servicio, podés hacer un fork y abrir un pull request.

---

## 📄 Licencia

Este proyecto es de uso libre. Podés usarlo, modificarlo y adaptarlo para tu negocio.
