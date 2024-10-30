from django.shortcuts import render
from .db import process_api_data
from .utils import api_consulta
import json

def home(request):
    return render(request, 'base.html', {})

def hola(request):
    return render(request, 'hola.html', {})

def api(request):
    response = api_consulta()
    list = json.loads(response["data"])
    db_response = process_api_data(list)
    return render(request, 'api.html', {"list":list, "db_response": db_response})