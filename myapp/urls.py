from django.urls import path
from . import views

urlpatterns = [
    path("", views.webpage1, name="login"),
    path("login.html", views.webpage1, name="login"),
    path("register.html", views.webpage2, name="register"),
    path("dashboard.html", views.webpage3, name="mainpage"),

    path('lists/', views.lists, name='lists'),
    path('receipts/', views.receipts, name='receipts'),
    path('reports/', views.reports, name='reports'),
]
