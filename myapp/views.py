from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View, ListView
from django.http import JsonResponse
from .models import *
import pyodbc

# Create your views here.
def connection():
    connect_key = "Driver={ODBC Driver 17 for SQL Server}; Server=localhost; Database=QLCDL; Trusted_Connection=yes;"
    conn = pyodbc.connect(connect_key)
    return conn
    
# manipulate Daily's data
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
    
# manipulate Daily's data
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
def DailyView(request):
    list_dl = Daily.objects.all()
    list_quan = Quan.objects.all()
    list_ldl = Loaidaily.objects.all()
    return render(request, 'daily.html', {'dailys': list_dl, 'quans': list_quan, 'ldls': list_ldl})
    
class CreateDaily(View):
    def get(self, request):
        tendl1 = request.GET.get('tendl', None) 
        maldl1 = request.GET.get('maldl', None)
        sdt1 = request.GET.get('sdt', None)
        dc1 = request.GET.get('dc', None)
        mq1 = request.GET.get('mq', None)
        ntn1 = request.GET.get('ntn', None)
        
        # Checking if this DAILY's name existed
        cursor = connection().cursor()
        cursor.execute("SELECT TENDAILY FROM DAILY")
        tendl_all = cursor.fetchall()
        cursor.close()

        for i in tendl_all:
            if i[0] == tendl1:
                data = {
                    'trungten': True
                }
                return JsonResponse(data)
        
        # Checking if this phone number existed
        cursor = connection().cursor()
        cursor.execute("SELECT DIENTHOAI FROM DAILY")
        sdt_all = cursor.fetchall()
        cursor.close()

        for i in sdt_all:
            if i[0] == sdt1:
                data = {
                    'trungsdt': True
                }
                return JsonResponse(data)
            
        # Generating DAILY'ID automatically
        cursor = connection().cursor()
        cursor.execute("SELECT MADAILY FROM DAILY")
        madl_all = cursor.fetchall()
        cursor.close()

        lst = []
        number = []
        for i in madl_all:
            lst.append(i[0])
        
        for i in lst:
            i = i.replace(" ",'')
            temp = i[2:]
            number.append(int(temp))
        
        max = int(0)
        for i in number:
            if i > max:
                max = i
        
        max += 1
        madl = "DL" + str(max)
        # Create new DAILY
        cursor = connection().cursor()
        cursor.execute("INSERT INTO DAILY VALUES(?,?,?,?,?,?,?,?)", madl, tendl1, maldl1, sdt1, dc1, mq1, ntn1, None)
        cursor.commit()
        cursor.close()
        
        data = {
            'new_dl': True
        }

        return JsonResponse(data)
        
class RemoveDaily(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        # DAILY existed in PHIEUXUATHANG list
        cursor = connection().cursor()
        cursor.execute("SELECT MADAILY FROM PHIEUXUATHANG")
        madl_pxh_all = cursor.fetchall()
        cursor.close()

        for i in madl_pxh_all:
            if(id1 == i[0]):
                data = {
                    'deleted': 'pxh'
                }
                return JsonResponse(data)

        # DAILY existed in PHIEUTHUTIEN list
        cursor = connection().cursor()
        cursor.execute("SELECT MADAILY FROM PHIEUTHUTIEN")
        madl_ptt_all = cursor.fetchall()
        cursor.close()

        for i in madl_ptt_all:
            if(id1 == i[0]):
                data = {
                    'deleted': 'ptt'
                }
                return JsonResponse(data)
        
        # DAILY existed in BAOCAOCONGNO list
        cursor = connection().cursor()
        cursor.execute("SELECT MADAILY FROM BAOCAOCONGNO")
        madl_bccn_all = cursor.fetchall()
        cursor.close()

        for i in madl_bccn_all:
            if(id1 == i[0]):
                data = {
                    'deleted': 'bccn'
                }
                return JsonResponse(data)
        
        # DAILY existed in BAOCAODOANHSO list
        cursor = connection().cursor()
        cursor.execute("SELECT MADAILY FROM BAOCAODOANHSO")
        madl_bcds_all = cursor.fetchall()
        cursor.close()

        for i in madl_bcds_all:
            if(id1 == i[0]):
                data = {
                    'deleted': 'bcds'
                }
                return JsonResponse(data)
            
        cursor = connection().cursor()
        cursor.execute("DELETE FROM DAILY WHERE MADAILY = ?", id1)
        cursor.commit()
        cursor.close()

        data = {
            'deleted': True
        }
        return JsonResponse(data)
        
class UpdateDaily(View):
    def get(self, request):
        id = request.GET.get('id', None)
        tendl1 = request.GET.get('tendl', None) 
        maldl1 = request.GET.get('maldl', None)
        sdt1 = request.GET.get('sdt', None)
        dc1 = request.GET.get('dc', None)
        mq1 = request.GET.get('mq', None)
        ntn1 = request.GET.get('ntn', None)

        # Checking if this DAILY's name existed
        cursor = connection().cursor()
        cursor.execute("SELECT TENDAILY FROM DAILY WHERE MADAILY<>?",id)
        tendl_all = cursor.fetchall()
        cursor.close()

        for i in tendl_all:
            if tendl1 == i[0]:
                data = {
                    'trungten': True
                }
                return JsonResponse(data)

        # Checking if this phone number existed
        cursor = connection().cursor()
        cursor.execute("SELECT DIENTHOAI FROM DAILY WHERE MADAILY<>?", id)
        sdt_all = cursor.fetchall()
        cursor.close()

        for i in sdt_all:
            if i[0] == sdt1:
                data = {
                    'trungsdt': True
                }
                return JsonResponse(data)

        # Update DAILY
        cursor = connection().cursor()
        cursor.execute("UPDATE DAILY SET TENDAILY=?, MALOAIDAILY=?, DIENTHOAI=?, DIACHI=?, MAQUAN=?, NGAYTIEPNHAN=? WHERE MADAILY=?", tendl1, maldl1, sdt1, dc1, mq1, ntn1, id)
        cursor.commit()
        cursor.close()

        data = {
            'daily_new': True
        }

        return JsonResponse(data)
        
class FindingDaily(View):
    def get(self, request):
        info = request.GET.get('info', None)
        inf = '%' + str(info) + '%'

        cursor = connection().cursor()
        cursor.execute("SELECT * FROM DAILY WHERE MADAILY LIKE ? OR TENDAILY LIKE ? OR MALOAIDAILY LIKE ? OR DIENTHOAI LIKE ? OR DIACHI LIKE ? OR MAQUAN LIKE ? OR NGAYTIEPNHAN LIKE ? OR SOTIENNO LIKE ?", inf, inf, inf, inf, inf, inf, inf, inf)
        dl_data = cursor.fetchall()
        cursor.close()

        if(dl_data == []):
            dl = {
                'dl': 'empty'
            }
            return JsonResponse(dl)
        
        data = []
        for i in dl_data:
            lst = []
            lst.append(i[0])
            lst.append(i[1])
            lst.append(i[2])
            lst.append(i[3])
            lst.append(i[4])
            lst.append(i[5])
            lst.append(i[6])
            lst.append(i[7])
            data.append(lst)
        
        dl = {
            'dl': data
        }
        return JsonResponse(dl)
        
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
        
class FindingLoaidaily(View):
    def get(self, request):
        info = request.GET.get('info', None)
        inf = '%' + str(info) + '%'

        cursor = connection().cursor()
        cursor.execute("SELECT * FROM LOAIDAILY WHERE MALOAIDAILY LIKE ? OR TENLOAIDAILY LIKE ? OR SONOTOIDA LIKE ?", inf, inf, inf)
        ldl_data = cursor.fetchall()
        cursor.close()

        if(ldl_data == []):
            ldl = {
                'ldl': 'empty'
            }
            return JsonResponse(ldl)
        
        data = []
        for i in ldl_data:
            lst = []
            lst.append(i[0])
            lst.append(i[1])
            lst.append(i[2])
            data.append(lst)
        
        ldl = {
            'ldl': data
        }
        return JsonResponse(ldl)
        
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
        
class FindQuan(View):
    def get(self, request):
        info = request.GET.get('info', None)
        inf = '%' + str(info) + '%'

        cursor = connection().cursor()
        cursor.execute("SELECT * FROM QUAN WHERE MAQUAN LIKE ? OR TENQUAN LIKE ?", inf, inf)
        quan_data = cursor.fetchall()
        cursor.close()

        if(quan_data == []):
            data_quan = {
                'data_quan': 'empty'
            }
            return JsonResponse(data_quan)
        
        data = []
        for i in quan_data:
            lst = []
            lst.append(i[0])
            lst.append(i[1])
            data.append(lst)
        
        data_quan = {
            'data_quan': data
        }
        return JsonResponse(data_quan)
        
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
        
class FindingMathang(View):
    def get(self, request):
        info = request.GET.get('info', None)
        inf = '%' + str(info) + '%'

        cursor = connection().cursor()
        cursor.execute("SELECT * FROM MATHANG WHERE MAMATHANG LIKE ? OR TENMATHANG LIKE ? OR MADVT LIKE ? OR SOLUONGTON LIKE ?", inf, inf, inf, inf)
        mh_data = cursor.fetchall()
        cursor.close()

        if(mh_data == []):
            mh = {
                'mh': 'empty'
            }
            return JsonResponse(mh)
        
        data = []
        for i in mh_data:
            lst = []
            lst.append(i[0])
            lst.append(i[1])
            lst.append(i[2])
            lst.append(i[3])
            data.append(lst)
        
        mh = {
            'mh': data
        }
        return JsonResponse(mh)
        
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
        
class FindDVT(View):
    def get(self, request):
        info = request.GET.get('info', None)
        inf = '%' + str(info) + '%'

        cursor = connection().cursor()
        cursor.execute("SELECT * FROM DVT WHERE MADVT LIKE ? OR TENDVT LIKE ?", inf, inf)
        dvt_data = cursor.fetchall()
        cursor.close()

        if(dvt_data == []):
            dvt = {
                'dvt': 'empty'
            }
            return JsonResponse(dvt)
        
        data = []
        for i in dvt_data:
            lst = []
            lst.append(i[0])
            lst.append(i[1])
            data.append(lst)
        
        dvt = {
            'dvt': data
        }
        return JsonResponse(dvt)
        
# manipulate PNH's data
class PNHView(ListView):
    model = Phieunhaphang
    template_name = 'pnh.html'
    context_object_name = 'pnhs'
    
class CreatePNH(View):
    def get(self, request):
        ngaylp = request.GET.get('date', None)

        cursor = connection().cursor()
        cursor.execute("SELECT MAPHIEUNHAP FROM PHIEUNHAPHANG")
        mapnh_all = cursor.fetchall()
        cursor.close()

        number = []
        lst = []

        for i in mapnh_all:
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
        mapnh = 'PNH' + str(max)

        cursor = connection().cursor()
        cursor.execute("INSERT INTO PHIEUNHAPHANG VALUES(?,?,?)", mapnh, ngaylp, None)
        cursor.commit()
        cursor.close()

        mathang = {
            'mapnh': mapnh,
        }

        data = {
            'pnh': mathang
        }

        return JsonResponse(data)
        
class RemovePNH(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        cursor = connection().cursor()
        cursor.execute("SELECT MAPHIEUNHAP FROM CT_PNH")
        mapnh_all = cursor.fetchall()
        cursor.close()

        for i in mapnh_all:
            if (id1 == i[0]):
                data = {
                    'deleted': False
                }
                return JsonResponse(data)

        cursor = connection().cursor()
        cursor.execute("DELETE FROM PHIEUNHAPHANG WHERE MAPHIEUNHAP = ?", id1)
        cursor.commit()
        cursor.close()

        data = {
            'deleted': True
        }
        return JsonResponse(data)
        
class UpdatePNH(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        date1 = request.GET.get('date', None)

        cursor = connection().cursor()
        cursor.execute("UPDATE PHIEUNHAPHANG SET NGAYLAPPHIEU=? WHERE MAPHIEUNHAP=?", date1, id1)
        cursor.commit()
        cursor.close()

        pnh = {'mapnh': id1}
        data = {
            'pnh': pnh
        }

        return JsonResponse(data)
        
class FindingPNH(View):
    def get(self, request):
        info = request.GET.get('info', None)
        inf = '%' + str(info) + '%'

        cursor = connection().cursor()
        cursor.execute("SELECT * FROM PHIEUNHAPHANG WHERE MAPHIEUNHAP LIKE ? OR NGAYLAPPHIEU LIKE ? OR TONGTIEN LIKE ?", inf, inf, inf)
        pnh_data = cursor.fetchall()
        cursor.close()

        if(pnh_data == []):
            pnh = {
                'pnh': 'empty'
            }
            return JsonResponse(pnh)
        
        data = []
        for i in pnh_data:
            lst = []
            lst.append(i[0])
            lst.append(i[1])
            lst.append(i[2])
            data.append(lst)
        
        pnh = {
            'pnh': data
        }
        return JsonResponse(pnh)
        
# manipulate PXH's data
def PXHView(request):
    list_daily = Daily.objects.all()
    list_pxh = Phieuxuathang.objects.all()
    return render(request, 'pxh.html', {'pxhs': list_pxh, 'dailys': list_daily})
    
class CreatePXH(View):
    def get(self, request):
        dl_id1 = request.GET.get('madl', None)
        ngaylp = request.GET.get('date', None)

        cursor = connection().cursor()
        cursor.execute("SELECT MAPHIEUXUAT FROM PHIEUXUATHANG")
        mapxh_all = cursor.fetchall()
        cursor.close()

        number = []
        lst = []

        for i in mapxh_all:
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
        mapxh = 'PXH' + str(max)

        cursor = connection().cursor()
        cursor.execute("INSERT INTO PHIEUXUATHANG VALUES(?,?,?,?)", mapxh, dl_id1, ngaylp, None)
        cursor.commit()
        cursor.close()

        mathang = {
            'mapxh': mapxh,
        }

        data = {
            'pxh': mathang
        }

        return JsonResponse(data)
        
class RemovePXH(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        cursor = connection().cursor()
        cursor.execute("SELECT MAPHIEUXUAT FROM CT_PXH")
        mapxh_all = cursor.fetchall()
        cursor.close()

        for i in mapxh_all:
            if (id1 == i[0]):
                data = {
                    'deleted': False
                }
                return JsonResponse(data)

        cursor = connection().cursor()
        cursor.execute("DELETE FROM PHIEUXUATHANG WHERE MAPHIEUXUAT = ?", id1)
        cursor.commit()
        cursor.close()

        data = {
            'deleted': True
        }
        return JsonResponse(data)
        
class UpdatePXH(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        dl_id1 = request.GET.get('madl', None)
        date1 = request.GET.get('date', None)

        cursor = connection().cursor()
        cursor.execute("UPDATE PHIEUXUATHANG SET MADAILY=?, NGAYLAPPHIEU=? WHERE MAPHIEUNHAP=?", dl_id1, date1, id1)
        cursor.commit()
        cursor.close()

        pxh = {'mapxh': id1}
        data = {
            'pnh': pxh
        }

        return JsonResponse(data)
        
class FindingPXH(View):
    def get(self, request):
        info = request.GET.get('info', None)
        inf = '%' + str(info) + '%'

        cursor = connection().cursor()
        cursor.execute("SELECT * FROM PHIEUXUATHANG WHERE MAPHIEUXUAT LIKE ? OR MADAILY LIKE ? OR NGAYLAPPHIEU LIKE ? OR TONGTIEN LIKE ?", inf, inf, inf, inf)
        pxh_data = cursor.fetchall()
        cursor.close()

        if(pxh_data == []):
            pxh = {
                'pxh': 'empty'
            }
            return JsonResponse(pxh)
        
        data = []
        for i in pxh_data:
            lst = []
            lst.append(i[0])
            lst.append(i[1])
            lst.append(i[2])
            lst.append(i[3])
            data.append(lst)
        
        pxh = {
            'pxh': data
        }
        return JsonResponse(pxh)
        
# manipulate PTT's data
def PTTView(request):
    list_daily = Daily.objects.all()
    list_ptt = Phieuthutien.objects.all()
    return render(request, 'ptt.html', {'ptts': list_ptt, 'dailys': list_daily})
    
class CreatePTT(View):
    def get(self, request):
        dl_id1 = request.GET.get('madl', None)
        ngaytt = request.GET.get('ngaytt', None)
        sotienthu = request.GET.get('sott', None)

        cursor = connection().cursor()
        cursor.execute("SELECT MAPHIEUTHUTIEN FROM PHIEUTHUTIEN")
        maptt_all = cursor.fetchall()
        cursor.close()

        lst = []
        number = []
        for i in maptt_all:
            lst.append(i[0])

        for i in lst:
            i = i.replace(" ", '')
            temp = i[3:]
            number.append(int(temp))

        max = 0
        for i in number:
            if i > max:
                max = i

        max += 1
        maptt = 'PTT' + str(max)

        cursor = connection().cursor()
        cursor.execute("INSERT INTO PHIEUTHUTIEN VALUES(?,?,?,?)", maptt, dl_id1, ngaytt, sotienthu)
        cursor.commit()
        cursor.close()

        mathang = {
            'mabccn': maptt,
        }

        data = {
            'ptt': mathang
        }
        return JsonResponse(data)
        
class RemovePTT(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        cursor = connection().cursor()
        cursor.execute("DELETE FROM PHIEUTHUTIEN WHERE MAPHIEUTHUTIEN = ?", id1)
        cursor.commit()
        cursor.close()

        data = {
            'deleted': True
        }
        return JsonResponse(data)
        
class UpdatePTT(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        dl_id1 = request.GET.get('dl_id', None)
        ngaytt = request.GET.get('date', None)
        sott = request.GET.get('money', None)

        cursor = connection().cursor()
        cursor.execute("UPDATE PHIEUTHUTIEN SET MADAILY=?, NGAYTHUTIEN=?, SOTIENTHU=?, WHERE MAPHIEUTHUTIEN=?", dl_id1, ngaytt, sott, id1)
        cursor.commit()
        cursor.close()

        ptt = {'maptt': id1}
        data = {
            'ptt': ptt
        }

        return JsonResponse(data)
        
class FindingPTT(View):
    def get(self, request):
        info = request.GET.get('info', None)
        inf = '%' + str(info) + '%'

        cursor = connection().cursor()
        cursor.execute("SELECT * FROM PHIEUTHUTIEN WHERE MAPHIEUTHUTIEN LIKE ? OR MADAILY LIKE ? OR NGAYTHUTIEN LIKE ? OR SOTIENTHU LIKE ?", inf, inf, inf, inf)
        ptt_data = cursor.fetchall()
        cursor.close()

        if(ptt_data == []):
            ptt = {
                'ptt': 'empty'
            }
            return JsonResponse(ptt)
        
        data = []
        for i in ptt_data:
            lst = []
            lst.append(i[0])
            lst.append(i[1])
            lst.append(i[2])
            lst.append(i[3])
            data.append(lst)
        
        ptt = {
            'ptt': data
        }
        return JsonResponse(ptt)
        
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
            itemp = i[0]
            itemp = itemp.replace(" ",'')
            if itemp == dl_id1:
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
        
class FindingBCCN(View):
    def get(self, request):
        info = request.GET.get('info', None)
        inf = '%' + str(info) + '%'

        cursor = connection().cursor()
        cursor.execute("SELECT * FROM BAOCAOCONGNO WHERE MABCCONGNO LIKE ? OR THANG LIKE ? OR MADAILY LIKE ? OR NODAU LIKE ? OR PHATSINH LIKE ? OR NOCUOI LIKE ?", inf, inf, inf, inf, inf, inf)
        bccn_data = cursor.fetchall()
        cursor.close()

        if(bccn_data == []):
            bccn = {
                'bccn': 'empty'
            }
            return JsonResponse(bccn)
        
        data = []
        for i in bccn_data:
            lst = []
            lst.append(i[0])
            lst.append(i[1])
            lst.append(i[2])
            lst.append(i[3])
            lst.append(i[4])
            lst.append(i[5])
            data.append(lst)
        
        bccn = {
            'bccn': data
        }
        return JsonResponse(bccn)
        
# manipulate BCDS's data
def BCDSView(request):
    list_bcds = Baocaodoanhso.objects.all()
    list_daily = Daily.objects.all()
    return render(request, 'bcds.html', {'bcdss': list_bcds, 'dailys': list_daily})
    
class CreateBCDS(View):
    def get(self, request):
        month = request.GET.get('thang', None)
        dl_id1 = request.GET.get('madl', None)

        cursor = connection().cursor()
        cursor.execute("SELECT MADAILY FROM BAOCAODOANHSO WHERE THANG=?", month)
        madl_thang_all = cursor.fetchall()
        cursor.close()

        for i in madl_thang_all:
            itemp = i[0]
            itemp.replace(" ",'')
            if dl_id1 == itemp:
                print("Yes")
                data = {
                    'bcds': ''
                }
                return JsonResponse(data)

        cursor = connection().cursor()
        cursor.execute("SELECT MABCDOANHSO FROM BAOCAODOANHSO")
        mabcds_all = cursor.fetchall()
        cursor.close()

        lst = []
        number = []
        for i in mabcds_all:
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
        mabcds_new = 'BCDS' + str(max)

        cursor = connection().cursor()
        cursor.execute("INSERT INTO BAOCAODOANHSO VALUES(?,?,?,?,?,?)", mabcds_new, month, dl_id1, None, None, None)
        cursor.commit()
        cursor.close()

        bcds = {
            'mabcds': mabcds_new,
        }

        data = {
            'bcds': bcds
        }
        return JsonResponse(data)
        
class RemoveBCDS(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        cursor = connection().cursor()
        cursor.execute("DELETE FROM BAOCAODOANHSO WHERE MABCDOANHSO = ?", id1)
        cursor.commit()
        cursor.close()

        data = {
            'deleted': True
        }
        return JsonResponse(data)
        
class UpdateBCDS(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        month1 = request.GET.get('month', None)
        dl_id1 = request.GET.get('dl_id', None)
        cursor = connection().cursor()
        cursor.execute("SELECT MADAILY FROM BAOCAODOANHSO WHERE THANG=?", month1)
        madl_thang_all = cursor.fetchall()
        cursor.close()

        for i in madl_thang_all:
            itemp = i[0]
            itemp = itemp.replace(" ",'')
            if dl_id1 == itemp:
                data = {
                    'bcds': ''
                }
                return JsonResponse(data)

        cursor = connection().cursor()
        cursor.execute("UPDATE BAOCAODOANHSO SET THANG=?, MADAILY=? WHERE MABCDOANHSO=?", month1, dl_id1, id1)
        cursor.commit()
        cursor.close()

        bcds = {'mabcdoanhso': id1}
        data = {
            'bcds': bcds
        }

        return JsonResponse(data)
        
class FindingBCDS(View):
    def get(self, request):
        info = request.GET.get('info', None)
        inf = '%' + str(info) + '%'

        cursor = connection().cursor()
        cursor.execute("SELECT * FROM BAOCAODOANHSO WHERE MABCDOANHSO LIKE ? OR THANG LIKE ? OR MADAILY LIKE ? OR SOPHIEUXUAT LIKE ? OR TONGTRIGIA LIKE ? OR TYLE LIKE ?", inf, inf, inf, inf, inf, inf)
        bcds_data = cursor.fetchall()
        cursor.close()

        if(bcds_data == []):
            bcds = {
                'bcds': 'empty'
            }
            return JsonResponse(bcds)
        
        data = []
        for i in bcds_data:
            lst = []
            lst.append(i[0])
            lst.append(i[1])
            lst.append(i[2])
            lst.append(i[3])
            lst.append(i[4])
            lst.append(i[5])
            data.append(lst)
        
        bcds = {
            'bcds': data
        }
        return JsonResponse(bcds)
        
# manipulate REG's data
class REGView(ListView):
    model = Thamso
    template_name = 'regulations.html'
    context_object_name = 'regs'
    
class UpdateREG(View):
    def get(self, request):
        
        dltoida = request.GET.get('sodlmax', None)
        tiledongia = request.GET.get('tldgban', None)

        cursor = connection().cursor()
        cursor.execute("UPDATE THAMSO SET SODAILYTOIDAMOIQUAN=?, TILEDONGIABAN=?", dltoida, tiledongia)
        cursor.commit()
        cursor.close()

        data = {
            'updated': dltoida
        }
        return JsonResponse(data)
        
# manipulate PCTNH's data
CTNH_pk = None

def PCTNHView(request):
    global CTNH_pk
    val = request.GET.get('id', None)
    list_mapnh = Phieunhaphang.objects.all()
    list_mamh = Mathang.objects.all()

    if val == None:
        val = CTNH_pk
        list_ct_pnh = CtPnh.objects.filter(maphieunhap=val)
    else:
        CTNH_pk = val
        return JsonResponse({'save': True})

    return render(request, 'QLCDL/pctnh.html', {'pctnhs': list_ct_pnh, 'mapnhs': list_mapnh, 'mamhs': list_mamh})
    
class CreatePCTNH(View):
    def get(self, request):
        global CTNH_pk
        mapnh = CTNH_pk
        mamh = request.GET.get('mamh', None)
        slnhap = request.GET.get('slnhap', None)
        dgnhap = request.GET.get('dgnhap', None)

        cursor = connection().cursor()
        cursor.execute("SELECT MACT_PNH FROM CT_PNH")
        mactpnh_all = cursor.fetchall()
        cursor.close()

        number = []
        lst = []

        for i in mactpnh_all:
            lst.append(i[0])

        for i in lst:
            i = i.replace(" ", '')
            temp = i[5:]
            number.append(int(temp))

        max = number[0]
        for i in number:
            if i > max:
                max = i

        max += 1
        mactpnh = 'CTPNH' + str(max)

        cursor = connection().cursor()
        cursor.execute("INSERT INTO CT_PNH VALUES(?,?,?,?,?,?)", mactpnh, mapnh, mamh, slnhap, dgnhap, None)
        cursor.commit()
        cursor.close()

        mathang = {
            'ct_pnh': mactpnh,
        }

        data = {
            'ct_pnh': mathang
        }

        return JsonResponse(data)
        
class RemovePCTNH(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        cursor = connection().cursor()
        cursor.execute("DELETE FROM CT_PNH WHERE MACT_PNH = ?", id1)
        cursor.commit()
        cursor.close()

        data = {
            'deleted': True
        }
        return JsonResponse(data)
        
class UpdatePCTNH(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        mapnh1 = request.GET.get('mapnh', None)
        mamh1 = request.GET.get('mamh', None)
        slnhap1 = request.GET.get('slnhap', None)
        dgnhap1 = request.GET.get('dgnhap', None)

        cursor = connection().cursor()
        cursor.execute("UPDATE CT_PNH SET MAPHIEUNHAP=?, MAMATHANG=?, SOLUONGNHAP=?, DONGIANHAP=? WHERE MACT_PNH=?", mapnh1, mamh1, slnhap1, dgnhap1, id1)
        cursor.commit()
        cursor.close()

        ct_pnh = {'ct_pnh': id1}
        data = {
            'ct_pnh': ct_pnh
        }

        return JsonResponse(data)
        
class FindingPCTNH(View):
    def get(self, request):
        info = request.GET.get('info', None)
        inf = '%' + str(info) + '%'

        cursor = connection().cursor()
        cursor.execute("SELECT * FROM CT_PNH WHERE MACT_PNH LIKE ? OR MAPHIEUNHAP LIKE ? OR MAMATHANG LIKE ? OR SOLUONGNHAP LIKE ? OR DONGIANHAP LIKE ? OR THANHTIEN LIKE ?", inf, inf, inf, inf, inf, inf)
        ctpnh_data = cursor.fetchall()
        cursor.close()

        if(ctpnh_data == []):
            ctpnh = {
                'ctpnh': 'empty'
            }
            return JsonResponse(ctpnh)
        
        data = []
        for i in ctpnh_data:
            lst = []
            lst.append(i[0])
            lst.append(i[1])
            lst.append(i[2])
            lst.append(i[3])
            lst.append(i[4])
            lst.append(i[5])
            data.append(lst)
        
        ctpnh = {
            'ctpnh': data
        }
        return JsonResponse(ctpnh)
        
# manipulate PCTXH's data
CTXH_pk = None

def PCTXHView(request):
    global CTXH_pk
    val = request.GET.get('id', None)
    list_mapxh = Phieuxuathang.objects.all()
    list_mamh = Mathang.objects.all()

    if val == None:
        val = CTXH_pk
        list_ct_pxh = CtPxh.objects.filter(maphieuxuat=val)
    else:
        CTXH_pk = val
        return JsonResponse({'save': True})

    return render(request, 'QLCDL/pctxh.html', {'pctxhs': list_ct_pxh, 'mapxhs': list_mapxh, 'mamhs': list_mamh})
    
class CreatePCTXH(View):
    def get(self, request):
        global CTXH_pk
        mapxh = CTXH_pk
        mamh = request.GET.get('mamh', None)
        slxuat = request.GET.get('slxuat', None)

        cursor = connection().cursor()
        cursor.execute("SELECT MACT_PXH FROM CT_PXH")
        mactpxh_all = cursor.fetchall()
        cursor.close()

        number = []
        lst = []

        for i in mactpxh_all:
            lst.append(i[0])

        for i in lst:
            i = i.replace(" ", '')
            temp = i[5:]
            number.append(int(temp))

        max = number[0]
        for i in number:
            if i > max:
                max = i

        max += 1
        mactpxh = 'CTPXH' + str(max)

        cursor = connection().cursor()
        cursor.execute("INSERT INTO CT_PXH VALUES(?,?,?,?,?,?)", mactpxh, mapxh, mamh, slxuat, None, None)
        cursor.commit()
        cursor.close()

        mathang = {
            'ct_pxh': mactpxh,
        }

        data = {
            'ct_pxh': mathang
        }

        return JsonResponse(data)
        
class RemovePCTXH(View):
    def get(self, request):
        id1 = request.GET.get('id', None)

        cursor = connection().cursor()
        cursor.execute("DELETE FROM CT_PXH WHERE MACT_PXH = ?", id1)
        cursor.commit()
        cursor.close()

        data = {
            'deleted': True
        }
        return JsonResponse(data)
        
class UpdatePCTXH(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        mapxh1 = request.GET.get('mapxh', None)
        mamh1 = request.GET.get('mamh', None)
        slxuat1 = request.GET.get('slxuat', None)

        cursor = connection().cursor()
        cursor.execute("UPDATE CT_PXH SET MAPHIEUXUAT=?, MAMATHANG=?, SOLUONGXUAT=? WHERE MACT_PXH=?", mapxh1, mamh1, slxuat1, id1)
        cursor.commit()
        cursor.close()

        ct_pxh = {'ct_pxh': id1}
        data = {
            'ct_pxh': ct_pxh
        }

        return JsonResponse(data)
        
class FindingPCTXH(View):
    def get(self, request):
        info = request.GET.get('info', None)
        inf = '%' + str(info) + '%'

        cursor = connection().cursor()
        cursor.execute("SELECT * FROM CT_PXH WHERE MACT_PXH LIKE ? OR MAPHIEUXUAT LIKE ? OR MAMATHANG LIKE ? OR SOLUONGXUAT LIKE ? OR DONGIAXUAT LIKE ? OR THANHTIEN LIKE ?", inf, inf, inf, inf, inf, inf)
        ctpxh_data = cursor.fetchall()
        cursor.close()

        if(ctpxh_data == []):
            ctpxh = {
                'ctpxh': 'empty'
            }
            return JsonResponse(ctpxh)
        
        data = []
        for i in ctpxh_data:
            lst = []
            lst.append(i[0])
            lst.append(i[1])
            lst.append(i[2])
            lst.append(i[3])
            lst.append(i[4])
            lst.append(i[5])
            data.append(lst)
        
        ctpxh = {
            'ctpxh': data
        }
        return JsonResponse(ctpxh)
