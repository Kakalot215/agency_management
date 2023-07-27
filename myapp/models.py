from django.db import models

class Baocaocongno(models.Model):
    mabccongno = models.CharField(db_column='MaBCCongNo', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    thang = models.SmallIntegerField(db_column='Thang')  # Field name made lowercase.
    madaily = models.ForeignKey('Daily', models.DO_NOTHING, db_column='MaDaiLy')  # Field name made lowercase.
    nodau = models.DecimalField(db_column='NoDau', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    phatsinh = models.DecimalField(db_column='PhatSinh', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    nocuoi = models.DecimalField(db_column='NoCuoi', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BaoCaoCongNo'


class Baocaodoanhso(models.Model):
    mabcdoanhso = models.CharField(db_column='MaBCDoanhSo', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    thang = models.SmallIntegerField(db_column='Thang')  # Field name made lowercase.
    madaily = models.ForeignKey('Daily', models.DO_NOTHING, db_column='MaDaiLy')  # Field name made lowercase.
    sophieuxuat = models.IntegerField(db_column='SoPhieuXuat', blank=True, null=True)  # Field name made lowercase.
    tongtrigia = models.DecimalField(db_column='TongTriGia', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    tyle = models.FloatField(db_column='TyLe', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BaoCaoDoanhSo'


class CtPnh(models.Model):
    mact_pnh = models.CharField(db_column='MaCT_PNH', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    maphieunhap = models.ForeignKey('Phieunhaphang', models.DO_NOTHING, db_column='MaPhieuNhap')  # Field name made lowercase.
    mamathang = models.ForeignKey('Mathang', models.DO_NOTHING, db_column='MaMatHang')  # Field name made lowercase.
    soluongnhap = models.IntegerField(db_column='SoLuongNhap')  # Field name made lowercase.
    dongianhap = models.DecimalField(db_column='DonGiaNhap', max_digits=19, decimal_places=4)  # Field name made lowercase.
    thanhtien = models.DecimalField(db_column='ThanhTien', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CT_PNH'


class CtPxh(models.Model):
    mact_pxh = models.CharField(db_column='MaCT_PXH', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    maphieuxuat = models.ForeignKey('Phieuxuathang', models.DO_NOTHING, db_column='MaPhieuXuat')  # Field name made lowercase.
    mamathang = models.ForeignKey('Mathang', models.DO_NOTHING, db_column='MaMatHang')  # Field name made lowercase.
    soluongxuat = models.IntegerField(db_column='SoLuongXuat')  # Field name made lowercase.
    dongiaxuat = models.DecimalField(db_column='DonGiaXuat', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    thanhtien = models.DecimalField(db_column='ThanhTien', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CT_PXH'


class Dvt(models.Model):
    madvt = models.CharField(db_column='MaDVT', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tendvt = models.CharField(db_column='TenDVT', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DVT'


class Daily(models.Model):
    madaily = models.CharField(db_column='MaDaiLy', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tendaily = models.CharField(db_column='TenDaiLy', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    maloaidaily = models.ForeignKey('Loaidaily', models.DO_NOTHING, db_column='MaLoaiDaiLy')  # Field name made lowercase.
    dienthoai = models.CharField(db_column='DienThoai', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    maquan = models.ForeignKey('Quan', models.DO_NOTHING, db_column='MaQuan')  # Field name made lowercase.
    ngaytiepnhan = models.DateTimeField(db_column='NgayTiepNhan')  # Field name made lowercase.
    sotienno = models.DecimalField(db_column='SoTienNo', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DaiLy'


class Loaidaily(models.Model):
    maloaidaily = models.CharField(db_column='MaLoaiDaiLy', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tenloaidaily = models.CharField(db_column='TenLoaiDaiLy', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sonotoida = models.DecimalField(db_column='SoNoToiDa', max_digits=19, decimal_places=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LoaiDaiLy'


class Mathang(models.Model):
    mamathang = models.CharField(db_column='MaMatHang', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tenmathang = models.CharField(db_column='TenMatHang', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    madvt = models.ForeignKey(Dvt, models.DO_NOTHING, db_column='MaDVT')  # Field name made lowercase.
    soluongton = models.IntegerField(db_column='SoLuongTon', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MatHang'


class Phieunhaphang(models.Model):
    maphieunhap = models.CharField(db_column='MaPhieuNhap', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    ngaylapphieu = models.DateTimeField(db_column='NgayLapPhieu')  # Field name made lowercase.
    tongtien = models.DecimalField(db_column='TongTien', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PhieuNhapHang'


class Phieuthutien(models.Model):
    maphieuthutien = models.CharField(db_column='MaPhieuThuTien', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    madaily = models.ForeignKey(Daily, models.DO_NOTHING, db_column='MaDaiLy')  # Field name made lowercase.
    ngaythutien = models.DateTimeField(db_column='NgayThuTien')  # Field name made lowercase.
    sotienthu = models.DecimalField(db_column='SoTienThu', max_digits=19, decimal_places=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PhieuThuTien'


class Phieuxuathang(models.Model):
    maphieuxuat = models.CharField(db_column='MaPhieuXuat', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    madaily = models.ForeignKey(Daily, models.DO_NOTHING, db_column='MaDaiLy')  # Field name made lowercase.
    ngaylapphieu = models.DateTimeField(db_column='NgayLapPhieu')  # Field name made lowercase.
    tongtien = models.DecimalField(db_column='TongTien', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PhieuXuatHang'


class Quyen(models.Model):
    maquyen = models.CharField(db_column='MaQuyen', primary_key=True, max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tenquyen = models.CharField(db_column='TenQuyen', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QUYEN'


class Quan(models.Model):
    maquan = models.CharField(db_column='MaQuan', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tenquan = models.CharField(db_column='TenQuan', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Quan'


class Taikhoan(models.Model):
    tentaikhoan = models.CharField(db_column='TenTaiKhoan', primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    matkhau = models.CharField(db_column='MatKhau', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    maquyen = models.ForeignKey(Quyen, models.DO_NOTHING, db_column='MaQuyen')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TAIKHOAN'


class Timkiem(models.Model):
    matimkiem = models.CharField(db_column='MaTimKiem', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TIMKIEM'


class Thamso(models.Model):
    sodailytoidamoiquan = models.IntegerField(db_column='SoDaiLyToiDaMoiQuan')  # Field name made lowercase.
    tiledongiaban = models.FloatField(db_column='TiLeDonGiaBan')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ThamSo'
