from django.urls import path
from . import views
from .views import ContratoListView

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('expired/', views.expired, name="expired"),
    path('expired-edur/', views.expirededur, name="expirededur"),
    path('report/', ContratoListView.as_view(), name='contratos_list'),
    path('api/', views.api, name = "api"),
    path('emilia/', views.emilia, name = "emilia"),
]
