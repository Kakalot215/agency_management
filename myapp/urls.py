from django.urls import path
from . import views

urlpatterns = [
    path("", views.webpage1, name="home"),
    path("register/", views.webpage2, name="register"),
    # URL for lists
    path("daily/", views.DailyView, name="daily_page"),
    path("loaidaily/", views.LoaidailyView.as_view(), name="loaidaily_page"),
    path("quan/", views.QuanView.as_view(), name="quan_page"),
    path("mathang/", views.MathangView.as_view(), name="mathang_page"),
    path("dvt/", views.DVTView.as_view(), name="dvt_page"),

    # URL for manipulating QUAN
    path("quan/create", views.CreateQuan.as_view(), name="quan_create"),
    path("quan/delete", views.RemoveQuan.as_view(), name="quan_remove"),
    path("quan/update", views.UpdateQuan.as_view(), name="quan_update"),

    # URL for manipulating DVT
    path("dvt/create", views.CreateDVT.as_view(), name="dvt_create"),
    path("dvt/delete", views.RemoveDVT.as_view(), name="dvt_remove"),
    path("dvt/update", views.UpdateDVT.as_view(), name="dvt_update"),

    # URL for manipulating LDL
    path("loaidaily/create", views.CreateLoaidaily.as_view(), name="ldl_create"),
    path("loaidaily/delete", views.RemoveLoaidaily.as_view(), name="ldl_remove"),
    path("loaidaily/update", views.UpdateLoaidaily.as_view(), name="ldl_update"),
    
    # URL for manipulating MATHANG
    path("mathang/create", views.CreateMathang.as_view(), name="mathang_create"),
    path("mathang/remove", views.RemoveMathang.as_view(), name="mathang_remove"),
    path("mathang/update", views.UpdateMathang.as_view(), name="mathang_update"),
    
    # URL for DAILY
    path("daily/create", views.CreateDaily.as_view(), name="daily_create"),
    path("daily/update", views.UpdateDaily.as_view(), name="daily_update"),
    path("daily/delete", views.RemoveDaily.as_view(), name="daily_remove"),

    # URL for bills
    path("pnh/", views.PNHView.as_view(), name="pnh_page"),
    path("pxh/", views.PXHView.as_view(), name="pxh_page"),
    path("pctnh/", views.PCTNHView.as_view(), name="pctnh_page"),
    path("pctxh/", views.PCTXHView.as_view(), name="pctxh_page"),
    path("ptt/", views.PTTView.as_view(), name="ptt_page"),

    # URL for reports
    path("bccn/", views.BCCNView, name="bccn_page"),
    path("bcds/", views.BCDSView, name="bcds_page"),

    # URL for manipulating BCCN
    path("bccn/create", views.CreateBCCN.as_view(), name="bccn_create"),
    path("bccn/delete", views.RemoveBCCN.as_view(), name="bccn_remove"),
    path("bccn/update", views.UpdateBCCN.as_view(), name="bccn_update"),

    #  URL for manipulating BCDS
    path("bcds/create", views.CreateBCDS.as_view(), name="bcds_create"),
    path("bcds/delete", views.RemoveBCDS.as_view(), name="bcds_remove"),
    path("bcds/update", views.UpdateBCDS.as_view(), name="bcds_update"),

    # URL for regulations
    path("regulations/", views.REGView.as_view(), name="regulations_page"),
    path("regulations/update", views.UpdateREG.as_view(), name="regulations_update"),
]
