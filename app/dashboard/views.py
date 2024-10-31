from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Contrato
from .db import process_api_data
from .utils import api_consulta
import json

def home(request):
    return render(request, 'navbar.html', {})

def expired(request):
    
    fecha_actual = timezone.now() - timedelta(days=1)
    
    # Filtra los contratos que aún no han vencido
    expired_contract = Contrato.objects.filter(
        fecha_de_fin_del_contrato__gte=fecha_actual
    ).order_by('fecha_de_fin_del_contrato')
    
    # Renderiza el template con el contexto
    return render(request, 'table_exp.html', {"expired_contract" : expired_contract})

def api(request):
    # response = api_consulta()
    list = Contrato.objects.all()
    #db_response = process_api_data(list)
    #return render(request, 'api.html', {"list":list, "db_response": db_response})
    return render(request, 'api.html', {"list":list})

def consulta(request):

    db_list = Contrato.objects.all()
    return render(request, 'dashboard.html', {"db_list":db_list})