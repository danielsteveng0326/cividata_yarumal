# app/login/urls.py
from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('check-auth/', views.check_auth_status, name='check_auth'),
]