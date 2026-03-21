import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

def enviar_m(email, nombre, fecha, hora, servicio, empleado, nota):

    user = str(st.secrets["emails"]["smtp_user"])
    password = str(st.secrets["emails"]["smtp_password"])


    msg = MIMEMultipart()
    msg['From'] = user          # ✅ Usá el email real como remitente
    msg['To']   = email
    msg['Subject'] = "Reserva de turno"

    mensaje = f"""
Hola {nombre},
Tu reserva fue realizada con éxito.
El día {fecha} a las {hora} horas.
Servicio elegido: {servicio}
Barbero: {empleado}

Te esperamos! Gracias.
    """

    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user, password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Error al enviar el mail: {e}")
        st.error(f"Error: {e}")