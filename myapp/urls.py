from django.urls import path
from QLCDL import views

urlpatterns = [
    path('', views.dashboard),
]
