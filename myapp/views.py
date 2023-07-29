from django.shortcuts import render
from .models import *
from django.contrib import messages
import pyodbc

def connection():
    connect_key = "Driver={ODBC Driver 17 for SQL Server}; Server=localhost; Database=QLCDL; Trusted_Connection=yes;"
    conn = pyodbc.connect(connect_key)
    return conn
    
def login(request):
    # Function used for loging in
    if request.method == "POST":
        usrname = request.POST["Uname"]
        passwd = request.POST["Pass"]

        cursor = connection().cursor()
        cursor.execute("SELECT * FROM TAIKHOAN")
        accounts = cursor.fetchall()
        for row in accounts:
            if usrname == row[0] and passwd == row[1]:
                return render(request, "dashboard.html", {})

        messages.error(request, "LogIn failed!")
    return render(request, "login.html", {})

def register(request):
    # Registering a new account
    if request.method == "POST":
        usrname = request.POST["username"]
        passwd = request.POST["password"]
        passwdagain = request.POST["passagain"]

        # Checking some constraints
        if (len(usrname) == 0):
            messages.error(request, "Your username is empty!")
            return render(request, "register.html")
        if (len(passwd) == 0):
            messages.error(request, "Your password is empty!")
            return render(request, "register.html")
        if(passwd != passwdagain):
            messages.error(request, "Your verified password is different from your password!")
            return render(request, "register.html")

        new_account = Taikhoan(tentaikhoan=usrname, matkhau=passwd, maquyentaikhoan='2')
        new_account.save()
        messages.success(request, "Register successfully!")

    return render(request, "register.html", {})

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
