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
    path("quan/finding", views.FindQuan.as_view(), name="quan_finding"),

    # URL for manipulating DVT
    path("dvt/create", views.CreateDVT.as_view(), name="dvt_create"),
    path("dvt/delete", views.RemoveDVT.as_view(), name="dvt_remove"),
    path("dvt/update", views.UpdateDVT.as_view(), name="dvt_update"),
    path("dvt/finding", views.FindDVT.as_view(), name="dvt_finding"),

    # URL for manipulating LDL
    path("loaidaily/create", views.CreateLoaidaily.as_view(), name="ldl_create"),
    path("loaidaily/delete", views.RemoveLoaidaily.as_view(), name="ldl_remove"),
    path("loaidaily/update", views.UpdateLoaidaily.as_view(), name="ldl_update"),
    path("loaidaily/finding", views.FindingLoaidaily.as_view(), name="ldl_finding"),
    
    # URL for manipulating MATHANG
    path("mathang/create", views.CreateMathang.as_view(), name="mathang_create"),
    path("mathang/remove", views.RemoveMathang.as_view(), name="mathang_remove"),
    path("mathang/update", views.UpdateMathang.as_view(), name="mathang_update"),
    path("mathang/finding", views.FindingMathang.as_view(), name="mathang_finding"),
    
    # URL for DAILY
    path("daily/create", views.CreateDaily.as_view(), name="daily_create"),
    path("daily/update", views.UpdateDaily.as_view(), name="daily_update"),
    path("daily/delete", views.RemoveDaily.as_view(), name="daily_remove"),
    path("daily/finding", views.FindingDaily.as_view(), name="daily_finding"),

    # URL for bills
    path("pnh/", views.PNHView.as_view(), name="pnh_page"),
    path("pxh/", views.PXHView, name="pxh_page"),
    path("pctnh/", views.PCTNHView, name="pctnh_page"),
    path("pctxh/", views.PCTXHView, name="pctxh_page"),
    path("ptt/", views.PTTView, name="ptt_page"),

    # URL for reports
    path("bccn/", views.BCCNView, name="bccn_page"),
    path("bcds/", views.BCDSView, name="bcds_page"),

    # URL for manipulating BCCN
    path("bccn/create", views.CreateBCCN.as_view(), name="bccn_create"),
    path("bccn/delete", views.RemoveBCCN.as_view(), name="bccn_remove"),
    path("bccn/update", views.UpdateBCCN.as_view(), name="bccn_update"),
    path("bccn/finding", views.FindingBCCN.as_view(), name="bccn_finding"),

    #  URL for manipulating BCDS
    path("bcds/create", views.CreateBCDS.as_view(), name="bcds_create"),
    path("bcds/delete", views.RemoveBCDS.as_view(), name="bcds_remove"),
    path("bcds/update", views.UpdateBCDS.as_view(), name="bcds_update"),
    path("bcds/finding", views.FindingBCDS.as_view(), name="bcds_finding"),

    # URL for manipulating PNH
    path("pnh/create", views.CreatePNH.as_view(), name="pnh_create"),
    path("pnh/remove", views.RemovePNH.as_view(), name="pnh_remove"),
    path("pnh/update", views.UpdatePNH.as_view(), name="pnh_update"),
    path("pnh/finding", views.FindingPNH.as_view(), name="pnh_finding"),

    # URL for manipulating PXH
    path("pxh/create", views.CreatePXH.as_view(), name="pxh_create"),
    path("pxh/remove", views.RemovePXH.as_view(), name="pxh_remove"),
    path("pxh/update", views.UpdatePXH.as_view(), name="pxh_update"),
    path("pxh/finding", views.FindingPXH.as_view(), name="pxh_finding"),

    # URL for manipulating PTT
    path("ptt/create", views.CreatePTT.as_view(), name="ptt_create"),
    path("ptt/remove", views.RemovePTT.as_view(), name="ptt_remove"),
    path("ptt/update", views.UpdatePTT.as_view(), name="ptt_update"),
    path("ptt/finding", views.FindingPTT.as_view(), name="ptt_finding"),

    # URL for regulations
    path("regulations/", views.REGView.as_view(), name="regulations_page"),
    path("regulations/update", views.UpdateREG.as_view(), name="regulations_update"),

    # URL for manipulating CT_PNH
    path("pctnh/create", views.CreatePCTNH.as_view(), name="pctnh_create"),
    path("pctnh/remove", views.RemovePCTNH.as_view(), name="pctnh_remove"),
    path("pctnh/update", views.UpdatePCTNH.as_view(), name="pctnh_update"),
    path("pctnh/finding", views.FindingPCTNH.as_view(), name="pctnh_finding"),

    # URL for manipulating CT_PXH
    path("pctxh/create", views.CreatePCTXH.as_view(), name="pctxh_create"),
    path("pctxh/remove", views.RemovePCTXH.as_view(), name="pctxh_remove"),
    path("pctxh/update", views.UpdatePCTXH.as_view(), name="pctxh_update"),
    path("pctxh/finding", views.FindingPCTXH.as_view(), name="pctxh_finding"),
]
