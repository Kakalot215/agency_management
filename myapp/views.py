from django.shortcuts import render
from .models import *

# ------------------------------------------- SELECT --------------------------------------------

def bc_congno(request):
    rec = Baocaocongno.objects.all()
    return render(request, )

def bc_doanhso(request):
    rec = Baocaodoanhso.objects.all()
    return render(request, )

def ct_pnh(request):
    rec = CtPnh.objects.all()
    return render(request, )

def ct_pxh(request):
    rec = CtPxh.objects.all()
    return render(request, )

def dvt(request):
    rec = Dvt.objects.all()
    return render(request, )

def daily(request):
    rec = Daily.objects.all()
    return render(request, )

def loaidaily(request):
    rec = Loaidaily.objects.all()
    return render(request, )

def mathang(request):
    rec = Mathang.objects.all()
    return render(request, )

def phieunhaphang(request):
    rec = Phieunhaphang.objects.all()
    return render(request, )

def phieuthutien(request):
    rec = Phieuthutien.objects.all()
    return render(request, )

def phieuxuathang(request):
    rec = Phieuxuathang.objects.all()
    return render(request, )

def quan(request):
    rec = Quan.objects.all()
    return render(request, )

def thamso(request):
    rec = Thamso.objects.all()
    return render(request, )

# ------------------------------------------- INSERT --------------------------------------------

# ------------------------------------------- DELETE --------------------------------------------

# ------------------------------------------- UPDATE --------------------------------------------
