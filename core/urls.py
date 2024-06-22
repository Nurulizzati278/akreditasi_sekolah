from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.index, name="index"),
    path("map/", views.map, name="map"),
    path("panduan_masyarakat/", views.panduan_masyarakat, name="panduan_masyarakat"),
    path("grafik/", views.grafik, name="grafik"),
    path("loginadmin/", views.loginadmin, name="loginadmin"),
    path("logoutadmin/", views.logoutadmin, name="logoutadmin"),
    path("user_login/", views.user_login, name="user_login"),
    # jangan ganggu yang baru
    # batassuci
    path("home/", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("DataSekolah/", views.DataSekolah, name="DataSekolah"),
    path("PengajuanSMA/", views.PengajuanSMA, name="PengajuanSMA"),
    path("PengajuanSMK/", views.PengajuanSMK, name="PengajuanSMK"),
    path("NilaiAkhir/",views.NilaiAkhir,name="NilaiAkhir"),
    path("PerbaruiAkreditasi/", views.PerbaruiAkreditasi, name="PerbaruiAkreditasi"),
    path("panduan/", views.panduan, name="panduan"),
    path("PengajuanSekolah/", views.PengajuanSekolah, name="PengajuanSekolah"),
    path("EditPengajuanSekolah/", views.EditPengajuanSekolah, name="EditPengajuanSekolah"),
]
