from __future__ import print_function
from django.db import models
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# Create your models here.
import datetime
import pickle
import os.path


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def buildService():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def listarEventos(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('Pegando proximos 10 eventos')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('Não existem proximos eventos.')
        return 'Não existem proximos eventos.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        return (start, event['summary'])

def criarEvento(service, assunto, local, descricao, dataInicio, dataFim):
    event = {
        'summary': assunto,
        'location': local,
        'description': descricao,
        'start': {
            'dateTime': dataInicio,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': dataFim,
            'timeZone': 'America/Los_Angeles',
        },
    }

    event = service.events().insert(calendarId='alex.silva@aluno.faculdadeimpacta.com.br', body=event).execute()
    print('Evento Criado: ' + (event.get('htmlLink')))
    

if __name__ == '__main__':
    service = buildService()

    listarEventos(service)

    criarEvento(service, 'a', 'b', 'c',  datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat())

    listarEventos(service)
