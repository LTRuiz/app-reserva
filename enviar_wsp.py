from twilio.rest import Client
import streamlit as st

def enviar_whatsapp(telefono, nombre, fecha, hora, servicio, empleado):
    account_sid = st.secrets["twilio"]["account_sid"]
    auth_token  = st.secrets["twilio"]["auth_token"]

    client = Client(account_sid, auth_token)

    mensaje = (
        f"✂ *DePelos · Confirmación de turno*\n\n"
        f"Hola {nombre}, tu turno fue reservado con éxito.\n\n"
        f"📅 Fecha: {fecha}\n"
        f"⏰ Hora: {hora}\n"
        f"💈 Servicio: {servicio}\n"
        f"👤 Profesional: {empleado}\n\n"
        f"Si necesitás cancelar, escribinos al 3549-000000."
    )

    client.messages.create(
        body=mensaje,
        from_="whatsapp:+14155238886",  # Número sandbox de Twilio
        to=f"whatsapp:+54{telefono}"    # Número del cliente con código de país
    )