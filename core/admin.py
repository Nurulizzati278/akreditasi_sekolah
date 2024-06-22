from django.contrib import admin, messages
from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers import serialize
from django.http import HttpResponse
from django import forms
from .models import *
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['nip', 'nama', 'is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('nip', 'nama')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Password', {'fields': ('password',)}),  # Menambahkan bagian untuk mengelola password
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nip', 'nama', 'is_active', 'is_staff', 'is_superuser', 'password1', 'password2'),
        }),
    )
    search_fields = ['nip', 'nama']
    ordering = ['nama']

admin.site.register(CustomUser, CustomUserAdmin)

class TemporaryPengajuanSekolahAdmin(admin.ModelAdmin):
    list_display = ('NPSN','NamaSekolah', 'NamaKepalaSekolah', 'NamaPengawasSekolah', 'AlamatSekolah', 'JumlahGuru', 'JumlahKelas', 'KabupatenKota' , 'Kecamatan', 'JenjangSekolah', 'StatusSekolah', 'AkreditasiSekolah', 'TahunPengajuanTerakhir', 'TanggalAjukan', 'StatusPengajuan','user')
    list_filter = ('StatusPengajuan', 'TanggalAjukan')
    actions = ['setujukan_pengajuan', 'tolak_pengajuan']

    def setujukan_pengajuan(self, request, queryset):
        for temporary_pengajuan in queryset:
            # Buat objek PengajuanSekolahModel dari TemporaryPengajuanSekolah
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
                TahunPengajuanTerakhir=temporary_pengajuan.TahunPengajuanTerakhir,
                user=temporary_pengajuan.user,
            )
            
            # Buat objek PolygonModel dari TemporaryPolygon
            temporary_polygon = TemporaryPolygon.objects.get(SekolahId=temporary_pengajuan)
            polygon = PolygonModel.objects.create(
                SekolahId=pengajuan_sekolah,
                geometri=temporary_polygon.geometri,
                warna=temporary_polygon.warna,
                user=temporary_pengajuan.user,
            )
            
            # Hapus objek dari model temporary
            temporary_pengajuan.delete()
            temporary_polygon.delete()

        self.message_user(request, f'{queryset.count()} pengajuan berhasil disetujui.')

    setujukan_pengajuan.short_description = 'Setujukan pengajuan terpilih'

    def tolak_pengajuan(self, request, queryset):
        for temporary_pengajuan in queryset:
            temporary_pengajuan.delete()
        self.message_user(request, f'{queryset.count()} pengajuan berhasil ditolak.')

    tolak_pengajuan.short_description = 'Tolak pengajuan terpilih'

admin.site.register(TemporaryPengajuanSekolah, TemporaryPengajuanSekolahAdmin)
admin.site.register(TemporaryPolygon)

class ApprovedPengajuanSekolahAdmin(admin.ModelAdmin):
    list_display = ('NPSN','NamaSekolah', 'NamaKepalaSekolah', 'NamaPengawasSekolah' ,'AlamatSekolah', 'KabupatenKota','Kecamatan', 'JenjangSekolah' ,'StatusSekolah', 'AkreditasiSekolah','TahunPengajuanTerakhir')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(status_pengajuan='disetujui')
    
admin.site.register(PengajuanSekolahModel, ApprovedPengajuanSekolahAdmin)
admin.site.register(PolygonModel)