from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st
from datetime import datetime

class GoogleCalendar:

    def __init__(self, credentials, idCalendar):
        self.credenciales = credentials
        self.idCalendar = idCalendar
        self.service = build("calendar","v3",
                             credentials= service_account.Credentials.from_service_account_info(self.credenciales, scopes = ["https://www.googleapis.com/auth/calendar"])
                             )

    def create_event (self, nom_event, inicio_event, final_event, timezone, attendees = None):

        event = {
            "summary": nom_event,
            "start": {
                "dateTime": inicio_event,
                "timeZone": timezone,
            },
            "end": {
                "dateTime": final_event,
                "timeZone": timezone,
            },
        }

        if attendees:
            event['attendees'] = [{"email": email} for email in attendees]
        
        try:
            evento_creado = self.service.events().insert(calendarId = self.idCalendar, body = event).execute()
        
        except HttpError as error:
            raise Exception(f"Se produjo un error: {error}")

        return evento_creado
    
    def get_events(self, date):
        time_min = f"{date}T00:00:00-03:00"
        time_max = f"{date}T23:59:59-03:00"
        result = self.service.events().list(
            calendarId=self.idCalendar,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        return result.get('items', [])

    def get_events_start_time(self, date):
        events = self.get_events(date)
        start_time=[]

        for event in events:
            start_dt = event["start"]["dateTime"]
            parsed = datetime.fromisoformat(start_dt[:-6])
            start_time.append(parsed.strftime("%H:%M"))
        return start_time
    
    def delete_event(self, event_id):
        try:
            self.service.events().delete(calendarId=self.idCalendar, eventId=event_id).execute()
        except HttpError as error:
            raise Exception(f"Se produjo un error al eliminar el evento: {error}")

# credentials = st.secrets["google"]["credenciales_google"]
# idCalendar = "lucasruiiz912@gmail.com"
# google = GoogleCalendar(credentials, idCalendar)
# start_date = "2026-03-20T12:00:00-03:00"
# end_date = "2026-03-20T13:00:00-03:00"
# timeZone = "America/Argentina/Cordoba"
# attendees = ""
# idevent = google.create_event("Turno reservado", start_date, end_date, timeZone, attendees)
# print(idevent)
# date = '2026-03-20'
# init_horas = google.get_events_start_time(date)
# print(init_horas)