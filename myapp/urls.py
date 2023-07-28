from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("login.html", views.login, name="login"),
    path("register.html", views.register, name="register"),
    path("dashboard.html", views.dashboard, name="mainpage"),

    path('lists/', views.lists, name='lists'),
    path('receipts/', views.receipts, name='receipts'),
    path('reports/', views.reports, name='reports'),
]
