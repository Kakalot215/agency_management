from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('lists/', views.lists, name='lists'),
    path('receipts/', views.receipts, name='receipts'),
    path('reports/', views.reports, name='reports'),
]
