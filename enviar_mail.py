import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

def enviar_m(email, nombre, fecha, hora, servicio, empleado, nota, uid):

    user = str(st.secrets["emails"]["smtp_user"])
    password = str(st.secrets["emails"]["smtp_password"])


    msg = MIMEMultipart()
    msg['From'] = user
    msg['To']   = email
    msg['Subject'] = "Reserva de turno"

    mensaje = f"""
Hola {nombre},
Tu reserva fue realizada con éxito.
El día {fecha} a las {hora} horas.
Servicio elegido: {servicio}
Barbero: {empleado}
———————————————————————
¿Necesitás cancelar tu turno?
Ingresá a la app, andá a la sección "Cancelar" e ingresá:

  · Email: {email}
  · Código de reserva: {uid}

Guardá este código, lo vas a necesitar para cancelar.
———————————————————————

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

def enviar_cancelacion(email, nombre, fecha, hora, servicio, empleado):

    user = str(st.secrets["emails"]["smtp_user"])
    password = str(st.secrets["emails"]["smtp_password"])

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To']   = email
    msg['Subject'] = "Cancelación de turno"

    mensaje = f"""
Hola {nombre},
Tu reserva fue cancelada correctamente.
El turno cancelado era el día {fecha} a las {hora} horas.
Servicio: {servicio}
Barbero: {empleado}

Si querés reservar un nuevo turno, podés hacerlo desde nuestra web.
Gracias!
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

def avisar_nuevo_turno(nombre, fecha, hora, servicio, empleado, nota):
    user = str(st.secrets["emails"]["smtp_user"])
    password = str(st.secrets["emails"]["smtp_password"])
    destinatario = str(st.secrets["emails"]["smtp_user"]) 

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To']   = destinatario
    msg['Subject'] = "Nueva reserva recibida"

    mensaje = f"""
Nueva reserva registrada:

Cliente: {nombre}
Fecha: {fecha} a las {hora}
Servicio: {servicio}
Barbero: {empleado}
Notas: {nota if nota else "Sin notas"}
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
        print(f"Error al avisar nuevo turno: {e}")


def avisar_cancelacion(nombre, fecha, hora, servicio, empleado):
    user = str(st.secrets["emails"]["smtp_user"])
    password = str(st.secrets["emails"]["smtp_password"])
    destinatario = str(st.secrets["emails"]["smtp_user"]) 

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To']   = destinatario
    msg['Subject'] = "Turno cancelado"

    mensaje = f"""
Un turno fue cancelado:

Cliente: {nombre}
Fecha: {fecha} a las {hora}
Servicio: {servicio}
Barbero: {empleado}
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
        print(f"Error al avisar cancelación: {e}")