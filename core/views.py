import json
import logging
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from .models import *
from .forms import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# masyarakat
def index(request):
    return render(request, "landing_page/index.html")


def map(request):
    # data_pengajuan = PengajuanSekolahModel.objects.all()
    data_poligon = PolygonModel.objects.all()

    # Kirim data ke template
    context = {"data_poligon": data_poligon}

    return render(request, "landing_page/map.html", context)


def grafik(request):
    data = PengajuanSekolahModel.objects.all()
    tahun_dict = {}  # Membuat dictionary untuk menyimpan data akreditasi berdasarkan tahun

    # Memproses data dan menggabungkan akreditasi untuk tahun yang sama
    for obj in data:
        if obj.TahunPengajuanTerakhir in tahun_dict:
            tahun_dict[obj.TahunPengajuanTerakhir]['A'] += obj.AkreditasiSekolah.count('A')
            tahun_dict[obj.TahunPengajuanTerakhir]['B'] += obj.AkreditasiSekolah.count('B')
            tahun_dict[obj.TahunPengajuanTerakhir]['C'] += obj.AkreditasiSekolah.count('C')
            tahun_dict[obj.TahunPengajuanTerakhir]['TT'] += obj.AkreditasiSekolah.count('TT')
        else:
            tahun_dict[obj.TahunPengajuanTerakhir] = {
                'A': obj.AkreditasiSekolah.count('A'),
                'B': obj.AkreditasiSekolah.count('B'),
                'C': obj.AkreditasiSekolah.count('C'),
                'TT': obj.AkreditasiSekolah.count('TT'),
            }

    tahun_list = []
    akreditasi_a = []
    akreditasi_b = []
    akreditasi_c = []
    akreditasi_tt = []

    # Mengurutkan tahun dan mengisi list dengan data dari dictionary
    for tahun in sorted(tahun_dict.keys()):
        akreditasi = tahun_dict[tahun]
        tahun_list.append(tahun)
        akreditasi_a.append(akreditasi['A'])
        akreditasi_b.append(akreditasi['B'])
        akreditasi_c.append(akreditasi['C'])
        akreditasi_tt.append(akreditasi['TT'])

    context = {
        'tahun_list': tahun_list,
        'akreditasi_a': akreditasi_a,
        'akreditasi_b': akreditasi_b,
        'akreditasi_c': akreditasi_c,
        'akreditasi_tt': akreditasi_tt,
    }
    return render(request, "landing_page/grafik.html", context)


def panduan_masyarakat(request):
    return render(request, "landing_page/panduan_masyarakat.html")


def loginadmin(request):
    return render(request, "core/login.html")


# fitur login
from django.contrib.auth import authenticate, login


def user_login(request):
    if request.method == "POST":
        nip = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, username=nip, password=password)

        if user is not None:
            # User terotentikasi, lakukan login
            login(request, user)
            # messages.success(request, "Anda berhasil login")
            return redirect("dashboard")  # Redirect setelah login berhasil
        else:
            # Autentikasi pengguna gagal
            messages.error(request, "Kamu salah Password dan Username.")
            return redirect("loginadmin")

    return render(request, "core/login.html")


# logout
def logoutadmin(request):
    logout(request)
    request.session.flush()
    return redirect("loginadmin")


def home(request):
    return render(request, "admin_sekolah/home.html")


@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
     # Ambil pengguna yang sedang login
    current_user = request.user

    # Ambil data PengajuanSekolahModel yang terkait dengan pengguna yang sedang login
    pengajuan_sekolah = PengajuanSekolahModel.objects.filter(user=current_user)
    
    # Periksa apakah pengguna memiliki pengajuan sekolah yang sudah disetujui
    data_disetujui = pengajuan_sekolah.exists() and pengajuan_sekolah.first().status_pengajuan == 'disetujui'

    data_poligon = PolygonModel.objects.all()

    # Mendapatkan semua pesan dari pesan framework
    all_messages = messages.get_messages(request)

    # Menyimpan pesan dalam list
    messages_to_delete = list(all_messages)

    context = {"data_poligon": data_poligon, 'pengajuan_sekolah': pengajuan_sekolah, 'data_disetujui': data_disetujui, 'messages': messages.get_messages(request)}
        
    return render(request, "admin_sekolah/dashboard.html", context)


def PengajuanSekolah(request):
    user = request.user

    if request.method == "POST":
        pengajuan_sekolah_form = PengajuanSekolahForm(request.POST, request.FILES)
        geojson_data = request.POST.get("geometri")
        warna = request.POST.get("warna")

        if pengajuan_sekolah_form.is_valid() and geojson_data:
            temporary_data = pengajuan_sekolah_form.save(commit=False)
            temporary_data.user = user
            temporary_data.save()

            # Simpan data poligon ke TemporaryPolygon
            temporary_polygon = TemporaryPolygon(
                SekolahId=temporary_data,
                geometri=geojson_data,
                warna=warna,
                user=user
            )
            temporary_polygon.save()
            
            messages.success(request, "Data Anda berhasil diajukan. Mohon tunggu untuk dilakukan persetujuan oleh admin.")
            return redirect("dashboard")
    else:
        pengajuan_sekolah_form = PengajuanSekolahForm()

    context = {"pengajuan_sekolah_form": pengajuan_sekolah_form}
    return render(request, "admin_sekolah/PengajuanSekolah.html", context)


def SetujukanPengajuan(request, temporary_pengajuan_id):
    # Ambil data pengajuan temporary berdasarkan ID
    temporary_pengajuan = TemporaryPengajuanSekolah.objects.get(pk=temporary_pengajuan_id)

    # Simpan data pengajuan sebagai PengajuanSekolahModel
    pengajuan_sekolah = PengajuanSekolahModel.objects.create(
        NPSN=temporary_pengajuan.NPSN,
        NamaSekolah=temporary_pengajuan.NamaSekolah,
        NamaKepalaSekolah=temporary_pengajuan.NamaKepalaSekolah,
        NamaPengawasSekolah=temporary_pengajuan.NamaPengawasSekolah,
        AlamatSekolah=temporary_pengajuan.AlamatSekolah,
        JumlahGuru=temporary_pengajuan.JumlahGuru,
        JumlahKelas=temporary_pengajuan.JumlahKelas,
        JenjangSekolah=temporary_pengajuan.JenjangSekolah,
        StatusSekolah=temporary_pengajuan.StatusSekolah,
        KabupatenKota=temporary_pengajuan.KabupatenKota,
        Kecamatan=temporary_pengajuan.Kecamatan,
        AkreditasiSekolah=temporary_pengajuan.AkreditasiSekolah,
        TahunPengajuanTerakhir = temporary_pengajuan.TahunPengajuanTerakhir,
        user=temporary_pengajuan.user_id, # Sertakan nilai user yang valid
        status_pengajuan="disetujui",
    )

    # Simpan data poligon ke PolygonModel
    temporary_polygon = TemporaryPolygon.objects.get(SekolahId=temporary_pengajuan)
    polygon = PolygonModel.objects.create(
        SekolahId=pengajuan_sekolah,  # Sesuaikan dengan nama field yang benar
        geometri=temporary_polygon.geometri,
        warna=temporary_polygon.warna,
        user_id=user_id
    )
    polygon.save()
    return render(request, "admin_sekolah/dashboard.html")


def TolakPengajuan(request, temporary_pengajuan_id):
    # Ambil data pengajuan temporary berdasarkan ID
    temporary_pengajuan = TemporaryPengajuanSekolah.objects.filter(pk=temporary_pengajuan_id).first()
    temporary_pengajuan.delete()

    return render(request, "admin_sekolah/dashboard.html")


def DataSekolah(request):
    items_per_page = 5
    data_sekolah = PengajuanSekolahModel.objects.all().order_by("SekolahId")

    # Ambil nilai parameter pencarian dari URL
    query = request.GET.get("q", "")

    # Jika ada parameter pencarian, filter data sesuai dengan akreditasi
    if query:
        data_sekolah = data_sekolah.filter(NamaSekolah__icontains=query)

    paginator = Paginator(data_sekolah, items_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"data_sekolah": page_obj, "query": query}
    return render(request, "admin_sekolah/DataSekolah.html", context)


def hitung_range_butir_1(guru_s1, total_guru):
    persentase = (guru_s1 / total_guru) * 100
    if persentase < 70:
        return 1
    elif persentase < 80:
        return 2
    elif persentase < 90:
        return 3
    else:
        return 4


def hitung_range_butir_2(guru_bersertifikat, total_guru):
    persentase = (guru_bersertifikat / total_guru) * 100
    if persentase < 55:
        return 1
    elif persentase < 70:
        return 2
    elif persentase < 85:
        return 3
    else:
        return 4


def hitung_range_butir_3(guru_mengajar, total_guru):
    persentase = (guru_mengajar / total_guru) * 100
    if persentase < 55:
        return 1
    elif persentase < 70:
        return 2
    elif persentase < 85:
        return 3
    else:
        return 4


def PengajuanSMA(request):
    if request.method == "POST":
        user = request.user
        # Ambil data dari form
        guru_s1 = int(request.POST.get("GuruS1"))
        total_guru_1 = int(request.POST.get("GuruKeseluruhan1"))
        guru_bersertifikat = int(request.POST.get("GuruBersertifikat"))
        total_guru_2 = int(request.POST.get("GuruKeseluruhan2"))
        guru_mengajar = int(request.POST.get("GuruMengajarSesuaiPendidikan"))
        total_guru_3 = int(request.POST.get("GuruKeseluruhan3"))

        # Hitung range untuk butir 1-3
        range_butir_1 = hitung_range_butir_1(guru_s1, total_guru_1)
        range_butir_2 = hitung_range_butir_2(guru_bersertifikat, total_guru_2)
        range_butir_3 = hitung_range_butir_3(guru_mengajar, total_guru_3)

        # Ambil pilihan pengguna untuk butir 4-9
        range_butir_4 = int(request.POST.get("ipr1"))
        range_butir_5 = int(request.POST.get("ipr2"))
        range_butir_6 = int(request.POST.get("ipr3"))
        range_butir_7 = int(request.POST.get("ipr4"))
        range_butir_8 = int(request.POST.get("ipr5"))
        range_butir_9 = int(request.POST.get("ipr6"))

        # Jumlahkan semua range
        jumlah_skor = (range_butir_1 + range_butir_2 + range_butir_3 + range_butir_4 + range_butir_5 + range_butir_6 + range_butir_7 + range_butir_8 + range_butir_9)

        nilai_Ipr = (jumlah_skor / 36) * 100

        # Ambil pilihan pengguna untuk butir 4-9
        range_butir_1 = int(request.POST.get("butir1"))
        range_butir_2 = int(request.POST.get("butir2"))
        range_butir_3 = int(request.POST.get("butir3"))
        range_butir_4 = int(request.POST.get("butir4"))
        range_butir_5 = int(request.POST.get("butir5"))
        range_butir_6 = int(request.POST.get("butir6"))
        range_butir_7 = int(request.POST.get("butir7"))
        range_butir_8 = int(request.POST.get("butir8"))
        range_butir_9 = int(request.POST.get("butir9"))
        range_butir_10 = int(request.POST.get("butir10"))
        range_butir_11 = int(request.POST.get("butir11"))
        jumlah_mutu_lulusan = (range_butir_1 + range_butir_2 + range_butir_3 + range_butir_4 + range_butir_5 + range_butir_6 + range_butir_7 + range_butir_8 + range_butir_9 + range_butir_10 + range_butir_11)
        nilai_kompoenen_mutu_lulusan = (jumlah_mutu_lulusan / 44) * 100
        nilai_mutu_lulusan = nilai_kompoenen_mutu_lulusan * (35 / 100)

        range_butir_12 = int(request.POST.get("butir12"))
        range_butir_13 = int(request.POST.get("butir13"))
        range_butir_14 = int(request.POST.get("butir14"))
        range_butir_15 = int(request.POST.get("butir15"))
        range_butir_16 = int(request.POST.get("butir16"))
        range_butir_17 = int(request.POST.get("butir17"))
        range_butir_18 = int(request.POST.get("butir18"))
        jumlah_proses_pembelajaran = (range_butir_12 + range_butir_13 + range_butir_14 + range_butir_15 + range_butir_16 + range_butir_17 + range_butir_18)
        nilai_kompoenen_proses_pembelajaran = (jumlah_proses_pembelajaran / 28) * 100
        nilai_proses_pembelajaran = nilai_kompoenen_proses_pembelajaran * (29 / 100)

        range_butir_19 = int(request.POST.get("butir19"))
        range_butir_20 = int(request.POST.get("butir20"))
        range_butir_21 = int(request.POST.get("butir21"))
        range_butir_22 = int(request.POST.get("butir22"))
        jumlah_mutu_guru = (range_butir_19 + range_butir_20 + range_butir_21 + range_butir_22)
        nilai_kompoenen_mutu_guru = (jumlah_mutu_guru / 16) * 100
        nilai_mutu_guru = nilai_kompoenen_mutu_guru * (18 / 100)

        range_butir_23 = int(request.POST.get("butir23"))
        range_butir_24 = int(request.POST.get("butir24"))
        range_butir_25 = int(request.POST.get("butir25"))
        range_butir_26 = int(request.POST.get("butir26"))
        range_butir_27 = int(request.POST.get("butir27"))
        range_butir_28 = int(request.POST.get("butir28"))
        range_butir_29 = int(request.POST.get("butir29"))
        range_butir_30 = int(request.POST.get("butir30"))
        range_butir_31 = int(request.POST.get("butir31"))
        range_butir_32 = int(request.POST.get("butir32"))
        range_butir_33 = int(request.POST.get("butir33"))
        range_butir_34 = int(request.POST.get("butir34"))
        range_butir_35 = int(request.POST.get("butir35"))
        jumlah_manajemen_sekolah = (range_butir_23 + range_butir_24 + range_butir_25 + range_butir_26 + range_butir_27 + range_butir_28 + range_butir_29 + range_butir_30 + range_butir_31 + range_butir_32 + range_butir_33 + range_butir_34 + range_butir_35)
        nilai_kompoenen_manajemen_sekolah = (jumlah_manajemen_sekolah / 52) * 100
        nilai_manajemen_sekolah = nilai_kompoenen_manajemen_sekolah * (18 / 100)

        jumlah_keseluruhan = (nilai_mutu_lulusan + nilai_proses_pembelajaran + nilai_mutu_guru + nilai_manajemen_sekolah)

        # Simpan nilai IPR ke dalam database
        pengajuan_sma = PengajuanSMAModel.objects.create(
            user_id=user,
            GuruS1=guru_s1,
            GuruKeseluruhan1=total_guru_1,
            GuruBersertifikat=guru_bersertifikat,
            GuruKeseluruhan2=total_guru_2,
            GuruMengajarSesuaiPendidikan=guru_mengajar,
            GuruKeseluruhan3=total_guru_3,
            HasilGurus1=range_butir_1,
            HasilGuruBersertifikat=range_butir_2,
            HasilGuruMengajarSesuaiPendidikan=range_butir_3,
            ipr4=range_butir_4,
            ipr5=range_butir_5,
            ipr6=range_butir_6,
            ipr7=range_butir_7,
            ipr8=range_butir_8,
            ipr9=range_butir_9,
            jumlah_skor=jumlah_skor,
            nilai_ipr=nilai_Ipr,
            butir1=range_butir_1,
            butir2=range_butir_2,
            butir3=range_butir_3,
            butir4=range_butir_4,
            butir5=range_butir_5,
            butir6=range_butir_6,
            butir7=range_butir_7,
            butir8=range_butir_8,
            butir9=range_butir_9,
            butir10=range_butir_10,
            butir11=range_butir_11,
            jumlah_mutu_lulusan=jumlah_mutu_lulusan,
            nilai_kompoenen_mutu_lulusan=nilai_kompoenen_mutu_lulusan,
            nilai_mutu_lulusan=nilai_mutu_lulusan,
            butir12=range_butir_12,
            butir13=range_butir_13,
            butir14=range_butir_14,
            butir15=range_butir_15,
            butir16=range_butir_16,
            butir17=range_butir_17,
            butir18=range_butir_18,
            jumlah_proses_pembelajaran=jumlah_proses_pembelajaran,
            nilai_kompoenen_proses_pembelajaran=nilai_kompoenen_proses_pembelajaran,
            nilai_proses_pembelajaran=nilai_proses_pembelajaran,
            butir19=range_butir_19,
            butir20=range_butir_20,
            butir21=range_butir_21,
            butir22=range_butir_22,
            jumlah_mutu_guru=jumlah_mutu_guru,
            nilai_kompoenen_mutu_guru=nilai_kompoenen_mutu_guru,
            nilai_mutu_guru=nilai_mutu_guru,
            butir23=range_butir_23,
            butir24=range_butir_24,
            butir25=range_butir_25,
            butir26=range_butir_26,
            butir27=range_butir_27,
            butir28=range_butir_28,
            butir29=range_butir_29,
            butir30=range_butir_30,
            butir31=range_butir_31,
            butir32=range_butir_32,
            butir33=range_butir_33,
            butir34=range_butir_34,
            butir35=range_butir_35,
            jumlah_manajemen_sekolah=jumlah_manajemen_sekolah,
            nilai_kompoenen_manajemen_sekolah=nilai_kompoenen_manajemen_sekolah,
            nilai_manajemen_sekolah=nilai_manajemen_sekolah,
            jumlah_keseluruhan=jumlah_keseluruhan,
        )
        pengajuan_sma.save()

        # Redirect ke views yang menampilkan nilai akhir
        return redirect("NilaiAkhir")
    else:
        return render(request, "admin_sekolah/PengajuanSMA.html")
    
def PengajuanSMK(request):
    if request.method == "POST":
        user = request.user
        # Ambil data dari form
        guru_s1 = int(request.POST.get("GuruS1"))
        total_guru_1 = int(request.POST.get("GuruKeseluruhan1"))
        guru_bersertifikat = int(request.POST.get("GuruBersertifikat"))
        total_guru_2 = int(request.POST.get("GuruKeseluruhan2"))
        guru_mengajar = int(request.POST.get("GuruMengajarSesuaiPendidikan"))
        total_guru_3 = int(request.POST.get("GuruKeseluruhan3"))

        # Hitung range untuk butir 1-3
        range_butir_1 = hitung_range_butir_1(guru_s1, total_guru_1)
        range_butir_2 = hitung_range_butir_2(guru_bersertifikat, total_guru_2)
        range_butir_3 = hitung_range_butir_3(guru_mengajar, total_guru_3)

        # Ambil pilihan pengguna untuk butir 4-9
        range_butir_4 = int(request.POST.get("ipr4"))
        range_butir_5 = int(request.POST.get("ipr5"))
        range_butir_6 = int(request.POST.get("ipr6"))
        range_butir_7 = int(request.POST.get("ipr7"))
        range_butir_8 = int(request.POST.get("ipr8"))
        range_butir_9 = int(request.POST.get("ipr9"))
        range_butir_10 = int(request.POST.get("ipr10"))

        # Jumlahkan semua range
        jumlah_skor = (range_butir_1 + range_butir_2 + range_butir_3 + range_butir_4 + range_butir_5 + range_butir_6 + range_butir_7 + range_butir_8 + range_butir_9 + range_butir_10)

        # Hitung nilai IPR
        nilai_Ipr = (jumlah_skor / 40) * 100

        # Ambil pilihan pengguna untuk butir 1-13
        range_butir_1 = int(request.POST.get("butir1"))
        range_butir_2 = int(request.POST.get("butir2"))
        range_butir_3 = int(request.POST.get("butir3"))
        range_butir_4 = int(request.POST.get("butir4"))
        range_butir_5 = int(request.POST.get("butir5"))
        range_butir_6 = int(request.POST.get("butir6"))
        range_butir_7 = int(request.POST.get("butir7"))
        range_butir_8 = int(request.POST.get("butir8"))
        range_butir_9 = int(request.POST.get("butir9"))
        range_butir_10 = int(request.POST.get("butir10"))
        range_butir_11 = int(request.POST.get("butir11"))
        range_butir_36 = int(request.POST.get("kekhususanbutir36"))
        range_butir_37 = int(request.POST.get("kekhususanbutir37"))
        jumlah_mutu_lulusan = (range_butir_1 + range_butir_2 + range_butir_3 + range_butir_4 + range_butir_5 + range_butir_6 + range_butir_7 + range_butir_8 + range_butir_9 + range_butir_10 + range_butir_11 + range_butir_36 + range_butir_37)
        nilai_kompoenen_mutu_lulusan = (jumlah_mutu_lulusan / 52) * 100
        nilai_mutu_lulusan = nilai_kompoenen_mutu_lulusan * (35 / 100)

        range_butir_12 = int(request.POST.get("butir12"))
        range_butir_13 = int(request.POST.get("butir13"))
        range_butir_14 = int(request.POST.get("butir14"))
        range_butir_15 = int(request.POST.get("butir15"))
        range_butir_16 = int(request.POST.get("butir16"))
        range_butir_17 = int(request.POST.get("butir17"))
        range_butir_18 = int(request.POST.get("butir18"))
        range_butir_38 = int(request.POST.get("kekhususanbutir38"))
        range_butir_39 = int(request.POST.get("kekhususanbutir39"))
        jumlah_proses_pembelajaran = (range_butir_12 + range_butir_13 + range_butir_14 + range_butir_15 + range_butir_16 + range_butir_17 + range_butir_18 + range_butir_38 + range_butir_39)
        nilai_kompoenen_proses_pembelajaran = (jumlah_proses_pembelajaran / 36) * 100
        nilai_proses_pembelajaran = nilai_kompoenen_proses_pembelajaran * (29 / 100)

        range_butir_19 = int(request.POST.get("butir19"))
        range_butir_20 = int(request.POST.get("butir20"))
        range_butir_21 = int(request.POST.get("butir21"))
        range_butir_22 = int(request.POST.get("butir22"))
        range_butir_40 = int(request.POST.get("kekhususanbutir40"))
        jumlah_mutu_guru = (range_butir_19 + range_butir_20 + range_butir_21 + range_butir_22 + range_butir_40)
        nilai_kompoenen_mutu_guru = (jumlah_mutu_guru / 20) * 100
        nilai_mutu_guru = nilai_kompoenen_mutu_guru * (18 / 100)

        range_butir_23 = int(request.POST.get("butir23"))
        range_butir_24 = int(request.POST.get("butir24"))
        range_butir_25 = int(request.POST.get("butir25"))
        range_butir_26 = int(request.POST.get("butir26"))
        range_butir_27 = int(request.POST.get("butir27"))
        range_butir_28 = int(request.POST.get("butir28"))
        range_butir_29 = int(request.POST.get("butir29"))
        range_butir_30 = int(request.POST.get("butir30"))
        range_butir_31 = int(request.POST.get("butir31"))
        range_butir_32 = int(request.POST.get("butir32"))
        range_butir_33 = int(request.POST.get("butir33"))
        range_butir_34 = int(request.POST.get("butir34"))
        range_butir_35 = int(request.POST.get("butir35"))
        range_butir_41 = int(request.POST.get("kekhususanbutir41"))
        range_butir_42 = int(request.POST.get("kekhususanbutir42"))
        range_butir_43 = int(request.POST.get("kekhususanbutir43"))
        range_butir_44 = int(request.POST.get("kekhususanbutir44"))
        jumlah_manajemen_sekolah = (range_butir_23 + range_butir_24 + range_butir_25 + range_butir_26 + range_butir_27 + range_butir_28 + range_butir_29 + range_butir_30 + range_butir_31 + range_butir_32 + range_butir_33 + range_butir_34 + range_butir_35 + range_butir_41 + range_butir_42 + range_butir_43 + range_butir_44)
        nilai_kompoenen_manajemen_sekolah = (jumlah_manajemen_sekolah / 68) * 100
        nilai_manajemen_sekolah = nilai_kompoenen_manajemen_sekolah * (18 / 100)

        jumlah_keseluruhan = (nilai_mutu_lulusan + nilai_proses_pembelajaran + nilai_mutu_guru + nilai_manajemen_sekolah)

        # Simpan nilai IPR ke dalam database
        pengajuan_smk = PengajuanSMKModel.objects.create(
            user_id=user,
            GuruS1=guru_s1,
            GuruKeseluruhan1=total_guru_1,
            GuruBersertifikat=guru_bersertifikat,
            GuruKeseluruhan2=total_guru_2,
            GuruMengajarSesuaiPendidikan=guru_mengajar,
            GuruKeseluruhan3=total_guru_3,
            HasilGurus1=range_butir_1,
            HasilGuruBersertifikat=range_butir_2,
            HasilGuruMengajarSesuaiPendidikan=range_butir_3,
            ipr4=range_butir_4,
            ipr5=range_butir_5,
            ipr6=range_butir_6,
            ipr7=range_butir_7,
            ipr8=range_butir_8,
            ipr9=range_butir_9,
            ipr10=range_butir_10,
            jumlah_skor=jumlah_skor,
            nilai_ipr=nilai_Ipr,
            butir1=range_butir_1,
            butir2=range_butir_2,
            butir3=range_butir_3,
            butir4=range_butir_4,
            butir5=range_butir_5,
            butir6=range_butir_6,
            butir7=range_butir_7,
            butir8=range_butir_8,
            butir9=range_butir_9,
            butir10=range_butir_10,
            butir11=range_butir_11,
            kekhususanbutir36=range_butir_36,
            kekhususanbutir37=range_butir_37, 
            jumlah_mutu_lulusan=jumlah_mutu_lulusan,
            nilai_kompoenen_mutu_lulusan=nilai_kompoenen_mutu_lulusan,
            nilai_mutu_lulusan=nilai_mutu_lulusan,
            butir12=range_butir_12,
            butir13=range_butir_13,
            butir14=range_butir_14,
            butir15=range_butir_15,
            butir16=range_butir_16,
            butir17=range_butir_17,
            butir18=range_butir_18,
            kekhususanbutir38=range_butir_38,
            kekhususanbutir39=range_butir_39,
            jumlah_proses_pembelajaran=jumlah_proses_pembelajaran,
            nilai_kompoenen_proses_pembelajaran=nilai_kompoenen_proses_pembelajaran,
            nilai_proses_pembelajaran=nilai_proses_pembelajaran,
            butir19=range_butir_19,
            butir20=range_butir_20,
            butir21=range_butir_21,
            butir22=range_butir_22,
            kekhususanbutir40=range_butir_40,
            jumlah_mutu_guru=jumlah_mutu_guru,
            nilai_kompoenen_mutu_guru=nilai_kompoenen_mutu_guru,
            nilai_mutu_guru=nilai_mutu_guru,
            butir23=range_butir_23,
            butir24=range_butir_24,
            butir25=range_butir_25,
            butir26=range_butir_26,
            butir27=range_butir_27,
            butir28=range_butir_28,
            butir29=range_butir_29,
            butir30=range_butir_30,
            butir31=range_butir_31,
            butir32=range_butir_32,
            butir33=range_butir_33,
            butir34=range_butir_34,
            butir35=range_butir_35,
            kekhususanbutir41=range_butir_41,
            kekhususanbutir42=range_butir_42,
            kekhususanbutir43=range_butir_43,
            kekhususanbutir44=range_butir_44,
            jumlah_manajemen_sekolah=jumlah_manajemen_sekolah,
            nilai_kompoenen_manajemen_sekolah=nilai_kompoenen_manajemen_sekolah,
            nilai_manajemen_sekolah=nilai_manajemen_sekolah,
            jumlah_keseluruhan=jumlah_keseluruhan,
        )
        pengajuan_smk.save()

        # Redirect ke views yang menampilkan nilai akhir
        return redirect("NilaiAkhir")
    else:
        return render(request, "admin_sekolah/PengajuanSMK.html")


def hitung_nilai_akhir(nilai_ipr, jumlah_keseluruhan):
    nilai_akhir = (nilai_ipr * 0.15) + (jumlah_keseluruhan * 0.85)
    return nilai_akhir


def tentukan_predikat(nilai_akhir):
    if nilai_akhir >= 91:
        return "A"
    elif nilai_akhir >= 81:
        return "B"
    elif nilai_akhir >= 71:
        return "C"
    else:
        return "D"


def NilaiAkhir(request):
    # Ambil user yang sedang melakukan request
    user = request.user

    # Query untuk mendapatkan objek pengajuan_sma terakhir yang terkait dengan user_id
    pengajuan_sma = PengajuanSMAModel.objects.filter(user_id=user.id).last()
    pengajuan_smk = PengajuanSMKModel.objects.filter(user_id=user.id).last()

    # Default nilai akhir dan predikat
    nilai_akhir = None
    predikat = None

    # Pastikan objek pengajuan_sma tidak None
    if pengajuan_sma:
        # Ambil nilai IPR dan jumlah keseluruhan dari objek pengajuan_sma
        nilai_ipr = pengajuan_sma.nilai_ipr
        jumlah_keseluruhan = pengajuan_sma.jumlah_keseluruhan

        # Hitung nilai akhir menggunakan fungsi hitung_nilai_akhir
        nilai_akhir = hitung_nilai_akhir(nilai_ipr, jumlah_keseluruhan)

        # Tentukan predikat
        predikat = tentukan_predikat(nilai_akhir)

    # Pastikan objek pengajuan_smk tidak None
    if pengajuan_smk:
        # Ambil nilai IPR dan jumlah keseluruhan dari objek pengajuan_smk
        nilai_ipr = pengajuan_smk.nilai_ipr
        jumlah_keseluruhan = pengajuan_smk.jumlah_keseluruhan

        # Hitung nilai akhir menggunakan fungsi hitung_nilai_akhir
        nilai_akhir = hitung_nilai_akhir(nilai_ipr, jumlah_keseluruhan)

        # Tentukan predikat
        predikat = tentukan_predikat(nilai_akhir)

    # Simpan nilai akhir dan predikat di database jika ada pengajuan
    if nilai_akhir is not None and predikat is not None:
        nilai_akhir_obj = NilaiAkhirModel.objects.create(
            user_id=user,
            nilai_akhir=nilai_akhir,
            predikat=predikat,
        )
        nilai_akhir_obj.save()

    return render(request,"admin_sekolah/NilaiAkhir.html",{"nilai_akhir": nilai_akhir, "predikat": predikat},)

def PerbaruiAkreditasi(request):
    if request.method == 'POST':
        # Ambil user yang sedang melakukan request
        user = request.user

        # Mendapatkan tahun saat ini
        tahun_sekarang = datetime.now().year

        # Lakukan perubahan pada tabel PengajuanSekolahModel untuk SMA
        pengajuan_sma = PengajuanSMAModel.objects.filter(user_id=user.id).last()
        if pengajuan_sma:
            predikat_baru_sma = tentukan_predikat(hitung_nilai_akhir(pengajuan_sma.nilai_ipr, pengajuan_sma.jumlah_keseluruhan))
            pengajuan_sekolah_sma = PengajuanSekolahModel.objects.filter(user_id=user.id, JenjangSekolah='SMA').last()
            if pengajuan_sekolah_sma:
                pengajuan_sekolah_sma.AkreditasiSekolah = predikat_baru_sma
                pengajuan_sekolah_sma.TahunPengajuanTerakhir = tahun_sekarang
                pengajuan_sekolah_sma.save()

        # Lakukan perubahan pada tabel PengajuanSekolahModel untuk SMK
        pengajuan_smk = PengajuanSMKModel.objects.filter(user_id=user.id).last()
        if pengajuan_smk:
            predikat_baru_smk = tentukan_predikat(hitung_nilai_akhir(pengajuan_smk.nilai_ipr, pengajuan_smk.jumlah_keseluruhan))
            pengajuan_sekolah_smk = PengajuanSekolahModel.objects.filter(user_id=user.id, JenjangSekolah='SMK').last()
            if pengajuan_sekolah_smk:
                pengajuan_sekolah_smk.AkreditasiSekolah = predikat_baru_smk
                pengajuan_sekolah_smk.TahunPengajuanTerakhir = tahun_sekarang
                pengajuan_sekolah_smk.save()

        # Lakukan perubahan pada tabel PolygonModel
        polygon = PolygonModel.objects.filter(user_id=user.id).last()
        if polygon:
            # Tentukan predikat baru (mungkin berbeda untuk SMA dan SMK)
            predikat_baru = predikat_baru_sma if pengajuan_sma else predikat_baru_smk
            
            # Tentukan warna baru berdasarkan predikat baru
            if predikat_baru == 'A':
                warna_baru = 'green'
            elif predikat_baru == 'B':
                warna_baru = 'blue'
            elif predikat_baru == 'C':
                warna_baru = 'yellow'
            else:
                warna_baru = 'red'
            
            # Perbarui warna poligon
            polygon.warna = warna_baru
            polygon.save()

        # Redirect atau lakukan apa pun yang diperlukan setelah penyimpanan berhasil

    return render(request, "admin_sekolah/PerbaruiAkreditasi.html")

def EditPengajuanSekolah(request):
    current_user = request.user
    pengajuan_sekolah = PengajuanSekolahModel.objects.get(user=current_user)

    if request.method == 'POST':
        edit_pengajuan_form = EditPengajuanSekolahForm(request.POST, instance=pengajuan_sekolah)
        if edit_pengajuan_form.is_valid():
            edit_pengajuan_form.save()
            return redirect('DataSekolah')
    else:
        edit_pengajuan_form = EditPengajuanSekolahForm(instance=pengajuan_sekolah)

    return render(request, 'admin_sekolah/EditPengajuanSekolah.html', {'edit_pengajuan_form': edit_pengajuan_form, 'pengajuan_sekolah': pengajuan_sekolah})

def panduan(request):
    return render(request, "admin_sekolah/panduan.html")
