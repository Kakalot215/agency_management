from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import HttpResponse

from .models import Taikhoan

# Import models for manipulate with lists
from .models import Daily
from .models import Loaidaily
from .models import Quan
from .models import Dvt
from .models import Mathang

# Import models for manipulate with bills
from .models import CtPxh
from .models import CtPnh
from .models import Phieunhaphang
from .models import Phieuthutien
from .models import Phieuxuathang

# Import models for manipulate with reports
from .models import Baocaocongno
from .models import Baocaodoanhso

# Import models for manipulate with regulations
from .models import Thamso

from django.contrib import messages
import pyodbc
from django.views.generic import View, ListView

# Create your views here.
def connection():
    connect_key = "Driver={ODBC Driver 17 for SQL Server}; Server=localhost; Database=QLCDL; Trusted_Connection=yes;"
    conn = pyodbc.connect(connect_key)
    return conn
def webpage1(request):
    # Function used for loging in
    if request.method == "POST":
        usrname = request.POST["Uname"]
        passwd = request.POST["Pass"]

        # Use API instead
        cursor = connection().cursor()
        cursor.execute("SELECT * FROM TAIKHOAN")
        accounts = cursor.fetchall()
        cursor.close()
        for row in accounts:
            if usrname == row[0] and passwd == row[1]:
                return redirect('daily_page')

        messages.error(request, "LogIn failed!")

    return render(request, "login.html", {})
def webpage2(request):
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

        # Checking if account is existed (not yet)


        new_account = Taikhoan(tentaikhoan=usrname, matkhau=passwd, maquyentaikhoan='2')
        new_account.save()
        messages.success(request, "Register successfully!")

    return render(request, "register.html", {})
# manipulate Daily's data
class DailyView(ListView):
    model = Daily
    template_name = 'daily.html'
    context_object_name = 'dailys'
class AddDaily(View):
    pass
class RemoveDaily(View):
    pass
class UpdateDaily(View):
    pass
# manipulate LOAIDAILY's data
class LoaidailyView(ListView):
    model = Loaidaily
    template_name = 'loaidaily.html'
    context_object_name = 'loaidailys'
class CreateLoaidaily(View):
    def get(self, request):
        tenldl = request.GET.get('name', None)
        sono = request.GET.get('debt', None)

        cursor = connection().cursor()
        cursor.execute("SELECT TENLOAIDAILY FROM LOAIDAILY")
        tenldl_all = cursor.fetchall()
        cursor.close()

        for i in tenldl_all:
            if i[0] == tenldl:
                data = {
                    'data': ''
                }
                return JsonResponse(data)
        
        cursor = connection().cursor()
        cursor.execute("SELECT MALOAIDAILY FROM LOAIDAILY")
        maldl_all = cursor.fetchall()
        cursor.close()

        number = []
        lst = []
        
        for i in maldl_all:
            lst.append(i[0])

        for i in lst:
            i = i.replace(" ", '')
            temp = i[3:]
            number.append(int(temp))

        max = number[0]
        for i in number:
            if i > max:
                max = i

        max += 1
        maldl = 'LDL' + str(max)

        obj = Loaidaily.objects.create(
            maloaidaily = maldl,
            tenloaidaily = tenldl,
            sonotoida = sono
        )

        ldl = {
            'maldl': obj.maloaidaily,
            'tenldl': obj.tenloaidaily,
            'sonotd': obj.sonotoida
        }

        data = {
            'ldl': ldl
        }

        return JsonResponse(data)
class RemoveLoaidaily(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        cursor = connection().cursor()
        cursor.execute("SELECT MALOAIDAILY FROM DAILY")
        maldl_all = cursor.fetchall()
        cursor.close()

        for i in maldl_all:
            if(id1 == i[0]):
                data = {
                    'deleted': False
                }
                return JsonResponse(data)

        cursor = connection().cursor()
        cursor.execute("DELETE FROM LOAIDAILY WHERE MALOAIDAILY = ?", id1)
        cursor.commit()
        cursor.close()

        data = {
            'deleted': True
        }
        return JsonResponse(data)
class UpdateLoaidaily(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('name', None)
        debt1 = request.GET.get('debt', None)

        cursor = connection().cursor()
        cursor.execute("SELECT TENLOAIDAILY FROM LOAIDAILY")
        tenldl_all = cursor.fetchall()
        cursor.close()

        for i in tenldl_all:
            if name1 == i[0]:
                data = {
                    'ldl': ''
                }
                return JsonResponse(data)

        print(id1)
        print(name1)
        print(debt1)
        obj = Loaidaily.objects.get(maloaidaily=id1)
        obj.tenloaidaily = name1
        obj.sonotoida = debt1
        obj.save()

        ldl = {'maquan': obj.maloaidaily, 'tenquan': obj.tenloaidaily, 'sonotoida': obj.sonotoida}
        data = {
            'ldl': ldl
        }
        return JsonResponse(data)
# manipulate QUAN's data
class QuanView(ListView):
    model = Quan
    template_name = 'quan.html'
    context_object_name = 'quans'
class CreateQuan(View):
    def get(self, request):
        tenquan_new = request.GET.get('tenquan', None)

        # Solving if tenquan existed
        cursor = connection().cursor()
        cursor.execute("SELECT TENQUAN FROM QUAN")
        tenquan_all = cursor.fetchall()
        cursor.close()

        for i in tenquan_all:
            if tenquan_new == i[0]:
                data = {
                    'quan': ''
                }
                return JsonResponse(data)

        # Solveing automatically generate maquan problem
        cursor = connection().cursor()
        cursor.execute("SELECT MAQUAN FROM QUAN")
        maquan_all = cursor.fetchall()
        cursor.close()

        number = []
        lst = []
        for i in maquan_all:
            lst.append(i[0])

        for i in lst:
            i = i.replace(" ","")
            temp = i[1:]
            number.append(int(temp))

        max = number[0]
        for i in number:
            if i > max:
                max = i
        max += 1
        maquan_new = 'Q' + str(max)

        obj = Quan.objects.create(
            maquan = maquan_new,
            tenquan = tenquan_new
        )
        quan_new = {'maquan': obj.maquan, 'tenquan': obj.tenquan}
        data = {
            'quan': quan_new
        }
        return JsonResponse(data)
class RemoveQuan(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        cursor = connection().cursor()
        cursor.execute("SELECT MAQUAN FROM DAILY")
        maquan_all = cursor.fetchall()
        cursor.close()

        for i in maquan_all:
            if(id1 == i[0]):
                data = {
                    'deleted': False
                }
                return JsonResponse(data)

        cursor = connection().cursor()
        cursor.execute("DELETE FROM QUAN WHERE MAQUAN = ?", id1)
        cursor.commit()
        cursor.close()

        data = {
            'deleted': True
        }
        return JsonResponse(data)
class UpdateQuan(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('name', None)

        cursor = connection().cursor()
        cursor.execute("SELECT TENQUAN FROM QUAN")
        tenquan_all = cursor.fetchall()
        cursor.close()

        for i in tenquan_all:
            if name1 == i[0]:
                data = {
                    'quan': ''
                }
                return JsonResponse(data)

        obj = Quan.objects.get(maquan=id1)
        obj.tenquan = name1
        obj.save()

        quan = {'maquan': obj.maquan, 'tenquan': obj.tenquan}
        data = {
            'quan': quan
        }

        return JsonResponse(data)
# manipulate Mathang's data
class MathangView(ListView):
    model = Mathang
    template_name = 'mathang.html'
    context_object_name = 'mathangs'
class CreateMathang(View):
    def get(self, request):
        name1 = request.GET.get('name', None)
        dvt_id1 = request.GET.get('dvt_id', None)
        tempvar = dvt_id1[12:-1]
        dvt_id1 = tempvar

        cursor = connection().cursor()
        cursor.execute("SELECT TENMATHANG FROM MATHANG")
        tenmh_all = cursor.fetchall()
        cursor.close()

        for i in tenmh_all:
            if i[0] == name1:
                data = {
                    'mathang': ''
                }
                return JsonResponse(data)

        cursor = connection().cursor()
        cursor.execute("SELECT MAMATHANG FROM MATHANG")
        mamh_all = cursor.fetchall()
        cursor.close()

        lst = []
        number = []
        for i in mamh_all:
            lst.append(i[0])
        
        for i in lst:
            i = i.replace(" ",'')
            temp = i[2:]
            number.append(int(temp))
        
        max = number[0]
        for i in number:
            if i > max:
                max = i

        max += 1
        mamh_new = 'MH' + str(max)

        cursor = connection().cursor()
        cursor.execute("INSERT INTO MATHANG VALUES(?,?,?,?)", mamh_new, name1, dvt_id1, None)
        cursor.commit()
        cursor.close()

        mathang = {
            'mamathang': mamh_new,
            'tenmathang': name1,
            'madvt': dvt_id1,
        }

        data = {
            'mathang': mathang
        }

        return JsonResponse(data)
class RemoveMathang(View):
    def get(self, request):
        mamh = request.GET.get('id' , None)

        cursor = connection().cursor()
        cursor.execute("SELECT MAMATHANG FROM CT_PNH")
        mamh_ctpnh = cursor.fetchall()
        cursor.execute("SELECT MAMATHANG FROM CT_PXH")
        mamh_ctpxh = cursor.fetchall()
        cursor.close()

        for i in mamh_ctpnh:
            if mamh == i[0]:
                check = 'CT_PNH'
                data = {
                'deleted': check
                }
                return JsonResponse(data)

        for i in mamh_ctpxh:
            if mamh == i[0]:
                check = 'CT_PXH'
                data = {
                'deleted': check
                }
                return JsonResponse(data) 

        cursor = connection().cursor()
        cursor.execute("DELETE FROM MATHANG WHERE MAMATHANG=?", mamh)
        cursor.commit()
        cursor.close()

        data = {
            'deleted': True
        }

        return JsonResponse(data)
class UpdateMathang(View):
    def get(self, request):
        id = request.GET.get('id', None)
        name = request.GET.get('name', None)
        mdvt = request.GET.get('dvt_id', None)

        tempvar = mdvt[12:-1]
        mdvt = tempvar

        cursor = connection().cursor()
        cursor.execute("SELECT TENMATHANG FROM MATHANG")
        tenmh_all = cursor.fetchall()
        cursor.close()

        for i in tenmh_all:
            if i[0] == name:
                data = {
                    'mathang': ''
                }
                return JsonResponse(data)

        cursor = connection().cursor()
        cursor.execute("UPDATE MATHANG SET TENMATHANG=?, MADVT=? WHERE MAMATHANG=?", name, mdvt, id)
        cursor.commit()
        cursor.close()

        mathang = {
            'mamathang': id
        }
        data = {
            'mathang': mathang
        }
        return JsonResponse(data)
# manipulate DVT's data
class DVTView(ListView):
    model = Dvt
    template_name = 'dvt.html'
    context_object_name = 'dvts'
class CreateDVT(View):
    def get(self, request):
        name1 = request.GET.get('name', None)

        cursor = connection().cursor()
        cursor.execute("SELECT TENDVT FROM DVT")
        tendvt_all = cursor.fetchall()
        cursor.close()

        for i in tendvt_all:
            if(name1 == i[0]):
                data = {
                    'dvt': ''
                }
                cursor.close()
                return JsonResponse(data)
        
        cursor = connection().cursor()
        cursor.execute("SELECT MADVT FROM DVT")
        madvt_all = cursor.fetchall()
        cursor.close()
        
        number = []
        lst = []

        for i in madvt_all:
            lst.append(i[0])
        
        for i in lst:
            i = i.replace(" ",'')
            temp = i[3:]
            number.append(int(temp))

        max = number[0]
        for i in number:
            if i > max:
                max = i
        
        max += 1
        madvt_new = 'DVT' + str(max)

        obj = Dvt.objects.create(
            madvt = madvt_new,
            tendvt = name1
        )

        print(obj.madvt)
        print(obj.tendvt)

        dvt = {
            'madvt': obj.madvt,
            'tendvt': obj.tendvt
        }

        data = {
            'dvt': dvt
        }

        return JsonResponse(data)
class RemoveDVT(View):
    def get(self, request):
        id = request.GET.get('id', None)

        cursor = connection().cursor()
        cursor.execute("SELECT MADVT FROM MATHANG")
        madvt_all = cursor.fetchall()
        cursor.close()

        for i in madvt_all:
            if i[0] == id:
                data = {
                    'deleted': False
                }
                return JsonResponse(data)
            
        cursor = connection().cursor()
        cursor.execute("DELETE FROM DVT WHERE MADVT=?", id)
        cursor.commit()
        cursor.close()

        data = {
            'deleted': True
        }

        return JsonResponse(data)
class UpdateDVT(View):
    def get(self, request):
        id = request.GET.get('id', None)
        name = request.GET.get('name', None)

        cursor = connection().cursor()
        cursor.execute("SELECT TENDVT FROM DVT")
        tendvt_all = cursor.fetchall()
        cursor.close()

        for i in tendvt_all:
            if i[0] == name:
                data = {
                    'dvt': ''
                }
                return JsonResponse(data)

        cursor = connection().cursor()
        cursor.execute("UPDATE DVT SET TENDVT=? WHERE MADVT=?", name, id)
        cursor.commit()
        cursor.close()

        dvt = {
            'mdvt': id
        }
        data = {
            'dvt': dvt
        }
        return JsonResponse(data)

class PNHView(ListView):
    model = Phieunhaphang
    template_name = 'pnh.html'
    context_object_name = 'pnhs'
class CreatePNH(View):
    pass
class RemovePNH(View):
    pass
class UpdatePNH(View):
    pass

class PXHView(ListView):
    model = Phieuxuathang
    template_name = 'pxh.html'
    context_object_name = 'pxhs'
class CreatePXH(View):
    pass
class RemovePXH(View):
    pass
class UpdatePXH(View):
    pass

class PCTNHView(ListView):
    model = CtPnh
    template_name = 'pctnh.html'
    context_object_name = 'ctpnhs'
class CreatePCTNH(View):
    pass
class RemovePCTNH(View):
    pass
class UpdatePCTNH(View):
    pass

class PCTXHView(ListView):
    model = CtPxh
    template_name = 'pctxh.html'
    context_object_name = 'ctpxhs'
class CreatePCTXH(View):
    pass
class RemovePCTXH(View):
    pass
class UpdatePCTXH(View):
    pass

class PTTView(ListView):
    model = Phieuthutien
    template_name = 'ptt.html'
    context_object_name = 'ptts'
class CreatePTT(View):
    pass
class RemovePTT(View):
    pass
class UpdatePTT(View):
    pass
# manipulate BCCN's data
def BCCNView(request):
    list_daily = Daily.objects.all() 
    list_bccn = Baocaocongno.objects.all()
    return render(request, 'bccn.html', {'bccns': list_bccn, 'dailys': list_daily})
class CreateBCCN(View):
    def get(self, request):
        month = request.GET.get('thang', None)
        dl_id1 = request.GET.get('madl', None)

        cursor = connection().cursor()
        cursor.execute("SELECT MADAILY FROM BAOCAOCONGNO WHERE THANG=?", month)
        madl_thang_all = cursor.fetchall()
        cursor.close()

        for i in madl_thang_all:
            if i[0] == dl_id1:
                data = {
                    'bccn': ''
                }
                return JsonResponse(data)

        cursor = connection().cursor()
        cursor.execute("SELECT MABCCONGNO FROM BAOCAOCONGNO")
        mabccn_all = cursor.fetchall()
        cursor.close()

        lst = []
        number = []
        for i in mabccn_all:
            lst.append(i[0])
        
        for i in lst:
            i = i.replace(" ",'')
            temp = i[4:]
            number.append(int(temp))
        
        max = 0
        for i in number:
            if i > max:
                max = i

        max += 1
        mabccn_new = 'BCCN' + str(max)

        cursor = connection().cursor()
        cursor.execute("INSERT INTO BAOCAOCONGNO VALUES(?,?,?,?,?,?)", mabccn_new, month, dl_id1, None, None, None)
        cursor.commit()
        cursor.close()

        mathang = {
            'mabccn': mabccn_new,
        }

        data = {
            'mabccn': mathang
        }
        return JsonResponse(data)
class RemoveBCCN(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        cursor = connection().cursor()
        cursor.execute("DELETE FROM BAOCAOCONGNO WHERE MABCCONGNO = ?", id1)
        cursor.commit()
        cursor.close()

        data = {
            'deleted': True
        }
        return JsonResponse(data)
class UpdateBCCN(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        month1 = request.GET.get('month', None)
        dl_id1 = request.GET.get('dl_id', None)

        cursor = connection().cursor()
        cursor.execute("SELECT MADAILY FROM BAOCAOCONGNO WHERE THANG=?", month1)
        madl_thang_all = cursor.fetchall()
        cursor.close()

        for i in madl_thang_all:
            if dl_id1 == i[0]:
                data = {
                    'bccn': ''
                }
                return JsonResponse(data)

        cursor = connection().cursor()
        cursor.execute("UPDATE BAOCAOCONGNO SET THANG=?, MADAILY=? WHERE MABCCONGNO=?", month1, dl_id1, id1)
        cursor.commit()
        cursor.close()

        bccn = {'mabccongno': id1}
        data = {
            'bccn': bccn
        }

        return JsonResponse(data)

class BCDSView(ListView):
    model = Baocaodoanhso
    template_name = 'bcds.html'
    context_object_name = 'bcdss'
class CreateBCDS(View):
    pass
class RemoveBCDS(View):
    pass
class UpdateBCDS(View):
    pass

class REGView(ListView):
    model = Thamso
    template_name = 'regulations.html'
    context_object_name = 'regs'
class CreateREG(View):
    pass
class RemoveREG(View):
    pass
class UpdateREG(View):
    pass
