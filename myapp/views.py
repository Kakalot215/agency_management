from django.shortcuts import render
from .models import *

def login(request):
    return render(request, 'myapp/login.html')

def register(request):
    return render(request, 'myapp/register.html')

def dashboard(request):
    return render(request, 'myapp/dashboard.html')

def lists(request):
    return render(request, 'QLCDL/lists.html')

def receipts(request):
    return render(request, 'QLCDL/receipts.html')

def reports(request):
    return render(request, 'QLCDL/reports.html')

# ------------------------------------------- SELECT --------------------------------------------

def bc_congno(request):
    rec = Baocaocongno.objects.all()
    return render(request, 'dashboard.html')

def bc_doanhso(request):
    rec = Baocaodoanhso.objects.all()
    return render(request, 'dashboard.html')

def ct_pnh(request):
    rec = CtPnh.objects.all()
    return render(request, 'dashboard.html')

def ct_pxh(request):
    rec = CtPxh.objects.all()
    return render(request, 'dashboard.html')

def dvt(request):
    rec = Dvt.objects.all()
    return render(request, 'dashboard.html')

def daily(request):
    rec = Daily.objects.all()
    return render(request, 'dashboard.html')

def loaidaily(request):
    rec = Loaidaily.objects.all()
    return render(request, 'dashboard.html')

def mathang(request):
    rec = Mathang.objects.all()
    return render(request, 'dashboard.html')

def phieunhaphang(request):
    rec = Phieunhaphang.objects.all()
    return render(request, 'dashboard.html')

def phieuthutien(request):
    rec = Phieuthutien.objects.all()
    return render(request, 'dashboard.html')

def phieuxuathang(request):
    rec = Phieuxuathang.objects.all()
    return render(request, 'dashboard.html')

def quan(request):
    rec = Quan.objects.all()
    return render(request, 'dashboard.html')

def thamso(request):
    rec = Thamso.objects.all()
    return render(request, 'dashboard.html')

# ------------------------------------------- INSERT --------------------------------------------

# ------------------------------------------- DELETE --------------------------------------------

# ------------------------------------------- UPDATE --------------------------------------------
