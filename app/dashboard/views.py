from django.shortcuts import render
from django.views.generic import ListView
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from .models import Contrato
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from .db import process_api_data
from .utils import api_consulta
from django.db.models.functions import Coalesce
from django.db.models import Value
from datetime import datetime
import json

#poner el id de la entidad
#edenorte = 727001372   #nit = 901831522
#municipio de yarumal = 704278142
#concejo de yarumal = 724167465


codigo_ent = 704278142
annoinicial=2025
annofinal=2025

def home(request):
    return render(request, 'navbar.html', {})

def dashboard(request):
    # Datos existentes
    suma_valor_del_contrato = Contrato.objects.filter(codigo_entidad=codigo_ent, fecha_de_firma__range=(datetime(annoinicial, 1, 1), datetime(annofinal, 12, 31, 23, 59, 59))).aggregate(Sum('valor_del_contrato'))['valor_del_contrato__sum']
    numero_de_registros = Contrato.objects.filter(codigo_entidad=codigo_ent, fecha_de_firma__range=(datetime(annoinicial, 1, 1), datetime(annofinal, 12, 31, 23, 59, 59))).count()
    numero_de_proveedores = Contrato.objects.filter(codigo_entidad=codigo_ent, fecha_de_firma__range=(datetime(annoinicial, 1, 1), datetime(annofinal, 12, 31, 23, 59, 59))).values('documento_proveedor').distinct().count()
    suma_valor_del_contrato = suma_valor_del_contrato//1000000
    
    # Consulta para obtener el número de contratos por mes
    contratos_por_mes = Contrato.objects.filter(codigo_entidad=codigo_ent).annotate(
        mes=TruncMonth('fecha_de_firma')
    ).values('mes').annotate(
        total=Count('id')
    ).order_by('mes')

    # Preparar datos para Chart.js
    labels = []
    data = []

    for item in contratos_por_mes:
        if item['mes']:
            labels.append(item['mes'].strftime('%B %Y'))  # Nombre del mes y año
            data.append(item['total'])

    # Obtener la suma de valores por mes
    valores_por_mes = Contrato.objects.filter(codigo_entidad=codigo_ent).annotate(
        mes=TruncMonth('fecha_de_firma')
    ).values('mes').annotate(
        total_valor=Sum('valor_del_contrato')  # Sumamos los valores
    ).order_by('mes')
    
    labels2 = []
    data2 = []

    for item in valores_por_mes:
        if item['mes']:
            mes = item['mes'].strftime('%B')
            labels2.append(mes)
            # Convertimos a millones para mejor visualización
            valor_en_millones = float(item['total_valor']) / 1000000
            data2.append(valor_en_millones)
    
    context = {
        'suma_valor_del_contrato': suma_valor_del_contrato,
        'numero_de_registros': numero_de_registros,
        'numero_de_proveedores': numero_de_proveedores,
        'labels': labels,
        'data': data,
        'labels2': labels2,
        'data2': data2,
    }

    return render(request, 'contract_dash.html', context)

def expired(request):
    
    fecha_actual = timezone.now() - timedelta(days=2)
    
    # Filtra los contratos que aún no han vencido
    expired_contract = Contrato.objects.filter(
        fecha_de_fin_del_contrato__gte=fecha_actual,
        codigo_entidad=codigo_ent
    ).order_by('fecha_de_fin_del_contrato')
    
    # Renderiza el template con el contexto
    return render(request, 'table_exp.html', {"expired_contract" : expired_contract})

def expirededur(request):
    
    fecha_actual = timezone.now() - timedelta(days=2)
    
    # Filtra los contratos que aún no han vencido
    expired_contract2 = Contrato.objects.filter(
        fecha_de_fin_del_contrato__gte=fecha_actual,
        documento_proveedor = '901831522'
    ).order_by('fecha_de_fin_del_contrato')
    
    # Renderiza el template con el contexto
    return render(request, 'table_expedur.html', {"expired_contract2" : expired_contract2})

def api(request):
    # Obtener datos de la API
    response = api_consulta()
    
    if response['status'] == 'success':
        # Convertir el JSON string a lista de diccionarios
        contratos_data = json.loads(response['data'])
        # Procesar los datos de la API
        nuevos, actualizados, errores = process_api_data(contratos_data)
        
        # Obtener la lista actualizada de contratos
        list = Contrato.objects.all()
        
        return render(request, 'api.html', {
            "list": list,
            "db_response": (nuevos, actualizados, errores),
            "success": True
        })
    else:
        return render(request, 'api.html', {
            "error": response['message'],
            "success": False
        })

def consulta(request):

    db_list = Contrato.objects.all()
    return render(request, 'dashboard.html', {"db_list":db_list})


class ContratoListView(ListView):
    model = Contrato
    template_name = 'table_report.html'
    context_object_name = 'contratos'

    def get_queryset(self):
        # Ordenar por fecha_de_firma de forma ascendente
        # Usando Coalesce para manejar fechas NULL
        return Contrato.objects.filter(codigo_entidad=codigo_ent, fecha_de_firma__range=(datetime(annoinicial, 1, 1), datetime(annofinal, 12, 31, 23, 59, 59))).annotate(
            fecha_orden=Coalesce('fecha_de_firma', Value(datetime.max))
        ).order_by('fecha_orden')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['columns'] = [
            {'field': 'referencia_del_contrato', 'title': 'Referencia del Contrato'},
            {'field': 'estado_contrato', 'title': 'Estado'},
            {'field': 'modalidad_de_contratacion', 'title': 'Modalidad de Contratación'},
            {'field': 'duracion_del_contrato', 'title': 'Duración'},
            {'field': 'fecha_de_firma', 'title': 'Fecha de Firma'},
            {'field': 'fecha_de_inicio_del_contrato', 'title': 'Fecha de Inicio'},
            {'field': 'fecha_de_fin_del_contrato', 'title': 'Fecha de Fin'},
            {'field': 'proveedor_adjudicado', 'title': 'Proveedor'},
            {'field': 'valor_del_contrato', 'title': 'Valor'},
            {'field': 'url_proceso', 'title': 'URL Proceso'},
            {'field': 'objeto_del_contrato', 'title': 'Objeto del Contrato'}
        ]
        return context
    
def emilia(request):
    return render(request, '', {})