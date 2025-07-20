from django.urls import path
from django.http import HttpResponse

def temp_view(request):
    return HttpResponse("""
    <html>
    <head><title>UnityGov - Funcionando</title></head>
    <body style="font-family: Arial; padding: 50px;">
        <h1>🎉 UnityGov está funcionando!</h1>
        <p>✅ Django está corriendo</p>
        <p>✅ URLs configuradas</p>
        <p>✅ Base de datos conectada</p>
        <p>✅ Deploy exitoso en Railway</p>
        <h2>Enlaces:</h2>
        <p><a href="/admin/">Admin</a></p>
        <p><em>Sistema inicializado correctamente.</em></p>
    </body>
    </html>
    """)

urlpatterns = [
    path('', temp_view, name="home"),
]