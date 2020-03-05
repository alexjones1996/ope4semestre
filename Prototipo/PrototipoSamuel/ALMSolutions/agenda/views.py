from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.shortcuts import render

SCOPES = ['https://www.googleapis.com/auth/calendar']


def index(request):
    return render(request, 'index.html')


def home(request):
    service = buildService()

    eventos = listarEventos(service)

    return render(request, 'eventos.html', {'eventos': eventos})


def agenda(request):
    return render(request, 'agenda.html')


def buildService():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('ALMSolutions/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def listarEventos(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()

    events = events_result.get('items', [])

    if not events:
        return 'Não existem proximos eventos.'
    return events


def criarEvento(service, assunto, local, descricao, dataInicio, dataFim):
    event = {
        'summary': assunto,
        'location': local,
        'description': descricao,
        'start': {
            'dateTime': dataInicio,
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': dataFim,
            'timeZone': 'America/Sao_Paulo',
        },
    }

    event = service.events().insert(calendarId='alex.silva@aluno.faculdadeimpacta.com.br', body=event).execute()
    return 'Evento criado com sucesso'
