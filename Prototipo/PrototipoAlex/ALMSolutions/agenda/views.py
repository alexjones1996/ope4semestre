from django.shortcuts import render
from django.http import HttpResponse
from .models import listarEventos, buildService

# Create your views here.
def home(request):
    return render(request,'index.html')

def agenda(request):
    return render(request,'agenda.html')

def eventos(request):
    
    service = buildService()
    lista_de_eventos = {'lista':listarEventos(service)}

    return render(request,'eventos.html', lista_de_eventos)
    #return HttpResponse('TESTE %  lista_de_eventos')