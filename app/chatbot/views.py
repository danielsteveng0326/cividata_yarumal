from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import requests
from django.conf import settings
import json

def chat_view(request):
    """Vista para renderizar la página del chatbot"""
    return render(request, 'chatbot/chat.html')

@require_http_methods(["POST"])
def process_message(request):
    """Vista para procesar los mensajes del usuario y obtener respuestas de la API de OpenAI"""
    try:
        user_message = request.POST.get('user_message')
        if not user_message:
            return JsonResponse({
                'error': 'No se proporcionó mensaje',
                'status': 'error'
            }, status=400)
        
        system_message = """
        Eres Emil-IA, un asistente profesional en derecho especializado en temas de contratación estatal de Colombia, 
        diseñado exclusivamente para el personal del Municipio de Yarumal. Tu objetivo es guiar a personas que no son 
        expertas en contratación estatal, ayudándoles a estructurar documentos clave para futuras contrataciones.

        Tus tareas principales son:
        1. Mejorar, modificar o crear el objeto de contratación
        2. Mejorar, modificar o crear la justificación de contratación (mínimo 500 palabras)
        3. Mejorar, modificar o crear las actividades específicas (mínimo 10 actividades detalladas)

        Si te preguntan sobre otros temas, responde cortésmente que solo puedes ayudar con temas de contratación estatal.
        """
        
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"Error en la API de OpenAI: {response.text}")
            
        response_data = response.json()
        assistant_response = response_data['choices'][0]['message']['content']
        
        return JsonResponse({
            'response': assistant_response,
            'status': 'success'
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)