from django import forms
from .models import *
from django.contrib.gis import forms as gis_forms

class PengajuanSekolahForm(forms.ModelForm):
    class Meta:
        model = TemporaryPengajuanSekolah
        fields = [
            "NPSN",
            "NamaSekolah",
            "NamaKepalaSekolah",
            "NamaPengawasSekolah",
            "JumlahGuru",
            "JumlahKelas",
            "AlamatSekolah",
            "JenjangSekolah",
            "StatusSekolah",
            "KabupatenKota",
            "Kecamatan",
            "AkreditasiSekolah",
            "TahunPengajuanTerakhir",
        ]
        
class EditPengajuanSekolahForm(forms.ModelForm):
    class Meta:
        model = PengajuanSekolahModel
        fields = [
            "NPSN",
            "NamaSekolah",
            "NamaKepalaSekolah",
            "NamaPengawasSekolah",
            "AlamatSekolah",
            "JumlahGuru",
            "JumlahKelas",
            "JenjangSekolah",
            "StatusSekolah",
            "KabupatenKota",
            "Kecamatan",
        ]