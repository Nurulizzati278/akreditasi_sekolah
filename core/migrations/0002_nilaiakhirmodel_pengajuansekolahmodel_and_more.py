# Generated by Django 5.0.6 on 2024-05-23 09:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NilaiAkhirModel',
            fields=[
                ('Nilaiid', models.BigAutoField(primary_key=True, serialize=False)),
                ('nilai_akhir', models.FloatField()),
                ('predikat', models.CharField(max_length=1)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PengajuanSekolahModel',
            fields=[
                ('SekolahId', models.BigAutoField(primary_key=True, serialize=False)),
                ('NPSN', models.BigIntegerField()),
                ('TanggalAjukan', models.DateField(auto_now_add=True, null=True)),
                ('NamaSekolah', models.CharField(max_length=250)),
                ('NamaKepalaSekolah', models.CharField(max_length=250)),
                ('NamaPengawasSekolah', models.CharField(max_length=250)),
                ('AlamatSekolah', models.CharField(max_length=600)),
                ('JenjangSekolah', models.CharField(choices=[('SMA', 'SMA'), ('SMK', 'SMK')], max_length=50)),
                ('StatusSekolah', models.CharField(choices=[('Negeri', 'Negeri'), ('Swasta', 'Swasta')], max_length=50)),
                ('KabupatenKota', models.CharField(choices=[('Kabupaten Aceh Barat', 'Kabupaten Aceh Barat'), ('Kabupaten Aceh Barat Daya', 'Kabupaten Aceh Barat Daya'), ('Kabupaten Aceh Besar', 'Kabupaten Aceh Besar'), ('Kabupaten Aceh Jaya', 'Kabupaten Aceh Jaya'), ('Kabupaten Aceh Selatan', 'Kabupaten Aceh Selatan'), ('Kabupaten Aceh Singkil', 'Kabupaten Aceh Singkil'), ('Kabupaten Aceh Tamiang', 'Kabupaten Aceh Tamiang'), ('Kabupaten Aceh Tengah', 'Kabupaten Aceh Tengah'), ('Kabupaten Aceh Tenggara', 'Kabupaten Aceh Tenggara'), ('Kabupaten Aceh Timur', 'Kabupaten Aceh Timur'), ('Kabupaten Aceh Utara', 'Kabupaten Aceh Utara'), ('Kabupaten Bener Meriah', 'Kabupaten Bener Meriah'), ('Kabupaten Bireun', 'Kabupaten Bireun'), ('Kabupaten Gayo Lues', 'Kabupaten Gayo Lues'), ('Kabupaten Nagan Raya', 'Kabupaten Nagan Raya'), ('Kabupaten Pidie', 'Kabupaten Pidie'), ('Kabupaten Pidie Jaya', 'Kabupaten Pidie Jaya'), ('Kabupaten Simeulue', 'Kabupaten Simeulue'), ('Kota Banda Aceh', 'Kota Banda Aceh'), ('Kota Langsa', 'Kota Langsa'), ('Kota Lhokseumawe', 'Kota Lhokseumawe'), ('Kota Sabang', 'Kota Sabang'), ('Kota Subulussalam', 'Kota Subulussalam')], max_length=600)),
                ('AkreditasiSekolah', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('TT', 'TT')], max_length=50)),
                ('TahunPengajuanTerakhir', models.IntegerField()),
                ('status_pengajuan', models.CharField(default='disetujui', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PengajuanSMAModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GuruS1', models.IntegerField()),
                ('GuruKeseluruhan1', models.IntegerField()),
                ('GuruBersertifikat', models.IntegerField()),
                ('GuruKeseluruhan2', models.IntegerField()),
                ('GuruMengajarSesuaiPendidikan', models.IntegerField()),
                ('GuruKeseluruhan3', models.IntegerField()),
                ('HasilGurus1', models.IntegerField()),
                ('HasilGuruBersertifikat', models.IntegerField()),
                ('HasilGuruMengajarSesuaiPendidikan', models.IntegerField()),
                ('ipr4', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('ipr5', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('ipr6', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('ipr7', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('ipr8', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('ipr9', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('jumlah_skor', models.FloatField()),
                ('nilai_ipr', models.FloatField()),
                ('butir1', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir2', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir3', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir4', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir5', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir6', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir7', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir8', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir9', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir10', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir11', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('jumlah_mutu_lulusan', models.IntegerField()),
                ('nilai_kompoenen_mutu_lulusan', models.IntegerField()),
                ('nilai_mutu_lulusan', models.IntegerField()),
                ('butir12', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir13', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir14', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir15', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir16', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir17', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir18', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('jumlah_proses_pembelajaran', models.IntegerField()),
                ('nilai_kompoenen_proses_pembelajaran', models.IntegerField()),
                ('nilai_proses_pembelajaran', models.IntegerField()),
                ('butir19', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir20', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir21', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir22', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('jumlah_mutu_guru', models.IntegerField()),
                ('nilai_kompoenen_mutu_guru', models.IntegerField()),
                ('nilai_mutu_guru', models.IntegerField()),
                ('butir23', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir24', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir25', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir26', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir27', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir28', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir29', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir30', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir31', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir32', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir33', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir34', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir35', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('jumlah_manajemen_sekolah', models.IntegerField()),
                ('nilai_kompoenen_manajemen_sekolah', models.IntegerField()),
                ('nilai_manajemen_sekolah', models.IntegerField()),
                ('jumlah_keseluruhan', models.IntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PengajuanSMKModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GuruS1', models.IntegerField()),
                ('GuruKeseluruhan1', models.IntegerField()),
                ('GuruBersertifikat', models.IntegerField()),
                ('GuruKeseluruhan2', models.IntegerField()),
                ('GuruMengajarSesuaiPendidikan', models.IntegerField()),
                ('GuruKeseluruhan3', models.IntegerField()),
                ('HasilGurus1', models.IntegerField()),
                ('HasilGuruBersertifikat', models.IntegerField()),
                ('HasilGuruMengajarSesuaiPendidikan', models.IntegerField()),
                ('ipr4', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('ipr5', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('ipr6', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('ipr7', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('ipr8', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('ipr9', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('ipr10', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('jumlah_skor', models.FloatField()),
                ('nilai_ipr', models.FloatField()),
                ('butir1', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir2', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir3', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir4', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir5', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir6', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir7', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir8', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir9', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir10', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir11', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('kekhususanbutir36', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('kekhususanbutir37', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('jumlah_mutu_lulusan', models.IntegerField()),
                ('nilai_kompoenen_mutu_lulusan', models.IntegerField()),
                ('nilai_mutu_lulusan', models.IntegerField()),
                ('butir12', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir13', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir14', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir15', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir16', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir17', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir18', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('kekhususanbutir38', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('kekhususanbutir39', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('jumlah_proses_pembelajaran', models.IntegerField()),
                ('nilai_kompoenen_proses_pembelajaran', models.IntegerField()),
                ('nilai_proses_pembelajaran', models.IntegerField()),
                ('butir19', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir20', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir21', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir22', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('kekhususanbutir40', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('jumlah_mutu_guru', models.IntegerField()),
                ('nilai_kompoenen_mutu_guru', models.IntegerField()),
                ('nilai_mutu_guru', models.IntegerField()),
                ('butir23', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir24', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir25', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir26', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir27', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir28', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir29', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir30', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir31', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir32', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir33', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir34', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('butir35', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('kekhususanbutir41', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('kekhususanbutir42', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('kekhususanbutir43', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('kekhususanbutir44', models.IntegerField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])),
                ('jumlah_manajemen_sekolah', models.IntegerField()),
                ('nilai_kompoenen_manajemen_sekolah', models.IntegerField()),
                ('nilai_manajemen_sekolah', models.IntegerField()),
                ('jumlah_keseluruhan', models.IntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PolygonModel',
            fields=[
                ('PolygonId', models.BigAutoField(primary_key=True, serialize=False)),
                ('geometri', models.JSONField()),
                ('warna', models.CharField(blank=True, max_length=20, null=True)),
                ('SekolahId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pengajuansekolahmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TemporaryPengajuanSekolah',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NPSN', models.BigIntegerField()),
                ('NamaSekolah', models.CharField(max_length=250)),
                ('NamaKepalaSekolah', models.CharField(max_length=250)),
                ('NamaPengawasSekolah', models.CharField(max_length=250)),
                ('AlamatSekolah', models.CharField(max_length=600)),
                ('JenjangSekolah', models.CharField(choices=[('SMA', 'SMA'), ('SMK', 'SMK')], max_length=50)),
                ('StatusSekolah', models.CharField(choices=[('Negeri', 'Negeri'), ('Swasta', 'Swasta')], max_length=50)),
                ('KabupatenKota', models.CharField(choices=[('Kabupaten Aceh Barat', 'Kabupaten Aceh Barat'), ('Kabupaten Aceh Barat Daya', 'Kabupaten Aceh Barat Daya'), ('Kabupaten Aceh Besar', 'Kabupaten Aceh Besar'), ('Kabupaten Aceh Jaya', 'Kabupaten Aceh Jaya'), ('Kabupaten Aceh Selatan', 'Kabupaten Aceh Selatan'), ('Kabupaten Aceh Singkil', 'Kabupaten Aceh Singkil'), ('Kabupaten Aceh Tamiang', 'Kabupaten Aceh Tamiang'), ('Kabupaten Aceh Tengah', 'Kabupaten Aceh Tengah'), ('Kabupaten Aceh Tenggara', 'Kabupaten Aceh Tenggara'), ('Kabupaten Aceh Timur', 'Kabupaten Aceh Timur'), ('Kabupaten Aceh Utara', 'Kabupaten Aceh Utara'), ('Kabupaten Bener Meriah', 'Kabupaten Bener Meriah'), ('Kabupaten Bireun', 'Kabupaten Bireun'), ('Kabupaten Gayo Lues', 'Kabupaten Gayo Lues'), ('Kabupaten Nagan Raya', 'Kabupaten Nagan Raya'), ('Kabupaten Pidie', 'Kabupaten Pidie'), ('Kabupaten Pidie Jaya', 'Kabupaten Pidie Jaya'), ('Kabupaten Simeulue', 'Kabupaten Simeulue'), ('Kota Banda Aceh', 'Kota Banda Aceh'), ('Kota Langsa', 'Kota Langsa'), ('Kota Lhokseumawe', 'Kota Lhokseumawe'), ('Kota Sabang', 'Kota Sabang'), ('Kota Subulussalam', 'Kota Subulussalam')], max_length=600)),
                ('AkreditasiSekolah', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('TT', 'TT')], max_length=50)),
                ('TahunPengajuanTerakhir', models.IntegerField()),
                ('TanggalAjukan', models.DateField(auto_now_add=True, null=True)),
                ('StatusPengajuan', models.CharField(choices=[('Menunggu', 'Menunggu'), ('Ditolak', 'Ditolak'), ('Disetujui', 'Disetujui')], default='Menunggu', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TemporaryPolygon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geometri', models.JSONField()),
                ('warna', models.CharField(blank=True, max_length=20, null=True)),
                ('SekolahId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.temporarypengajuansekolah')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]