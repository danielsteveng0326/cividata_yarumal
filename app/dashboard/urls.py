from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('hola/', views.hola, name="hola"),
    path('api/', views.api, name = "api"),
]