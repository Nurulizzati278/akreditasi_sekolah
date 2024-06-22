from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models

import os
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, nip, nama, umur, golongan, password=None):
        if not nip:
            raise ValueError("NIP field must be set")
        user = self.model(
            nip=nip,
            nama=nama,
        )
        user.set_password(password)  # hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, nip, nama, umur, golongan, password=None):
        user = self.create_user(
            nip=nip,
            nama=nama,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    nip = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        related_name="customuser_groups",  # Ubah related_name di sini
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        related_name="customuser_permissions",  # Ubah related_name di sini
    )

    objects = CustomUserManager()

    # Use NIP as the username field
    USERNAME_FIELD = "nip"
    REQUIRED_FIELDS = ["nama", "umur", "golongan"]

    def __str__(self):
        return self.nama

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class TemporaryPengajuanSekolah(models.Model):
    KABUPATENKOTA_CHOICES = [
        ('Kabupaten Aceh Barat','Kabupaten Aceh Barat'),
        ('Kabupaten Aceh Barat Daya','Kabupaten Aceh Barat Daya'),
        ('Kabupaten Aceh Besar','Kabupaten Aceh Besar'),
        ('Kabupaten Aceh Jaya','Kabupaten Aceh Jaya'),
        ('Kabupaten Aceh Selatan','Kabupaten Aceh Selatan'),
        ('Kabupaten Aceh Singkil','Kabupaten Aceh Singkil'),
        ('Kabupaten Aceh Tamiang','Kabupaten Aceh Tamiang'),
        ('Kabupaten Aceh Tengah','Kabupaten Aceh Tengah'),
        ('Kabupaten Aceh Tenggara','Kabupaten Aceh Tenggara'),
        ('Kabupaten Aceh Timur','Kabupaten Aceh Timur'),
        ('Kabupaten Aceh Utara','Kabupaten Aceh Utara'),
        ('Kabupaten Bener Meriah','Kabupaten Bener Meriah'),
        ('Kabupaten Bireun','Kabupaten Bireun'),
        ('Kabupaten Gayo Lues','Kabupaten Gayo Lues'),
        ('Kabupaten Nagan Raya','Kabupaten Nagan Raya'),
        ('Kabupaten Pidie','Kabupaten Pidie'),
        ('Kabupaten Pidie Jaya','Kabupaten Pidie Jaya'),
        ('Kabupaten Simeulue','Kabupaten Simeulue'),
        ('Kota Banda Aceh','Kota Banda Aceh'),
        ('Kota Langsa','Kota Langsa'),
        ('Kota Lhokseumawe','Kota Lhokseumawe'),
        ('Kota Sabang','Kota Sabang'),
        ('Kota Subulussalam','Kota Subulussalam'),
    ]
    
    KECAMATAN_CHOICES = {
        'Kabupaten Aceh Barat': [
            ('Kecamatan Arongan Lambalek', 'Kecamatan Arongan Lambalek'),
            ('Kecamatan Bubon', 'Kecamatan Bubon'),
            ('Kecamatan Johan Pahlawan', 'Kecamatan Johan Pahlawan'),
            ('Kecamatan Kaway XVI', 'Kecamatan Kaway XVI'),
            ('Kecamatan Meureubo', 'Kecamatan Meureubo'),
            ('Kecamatan Pante Ceureumen', 'Kecamatan Pante Ceureumen'),
            ('Kecamatan Panton reu', 'Kecamatan Panton reu'),
            ('Kecamatan Samatiga', 'Kecamatan Samatiga'),
            ('Kecamatan Sungai Mas', 'Kecamatan Sungai Mas'),
            ('Kecamatan Woyla', 'Kecamatan Woyla'),
            ('Kecamatan Woyla Barat', 'Kecamatan Woyla Barat'),
            ('Kecamatan Woyla Timur', 'Kecamatan Woyla Timur'),
        ],
        'Kabupaten Aceh Barat Daya': [
            ('Kecamatan Babahrot', 'Kecamatan Babahrot'),
            ('Kecamatan Blang Pidie', 'Kecamatan Blang Pidie'),
            ('Kecamatan Jeumpa', 'Kecamatan Jeumpa'),
            ('Kecamatan Kuala Batee', 'Kecamatan Kuala Batee'),
            ('Kecamatan Lembah Sabil', 'Kecamatan Lembah Sabil'),
            ('Kecamatan Manggeng', 'Kecamatan Manggeng'),
            ('Kecamatan Setia', 'Kecamatan Setia'),
            ('Kecamatan Susoh', 'Kecamatan Susoh'),
            ('Kecamatan Tangan Tangan', 'Kecamatan Tangan Tangan'),
        ],
        'Kabupaten Aceh Besar': [
            ('Kecamatan Baitussalam', 'Kecamatan Baitussalam'),
            ('Kecamatan Blang Bintang', 'Kecamatan Blang Bintang'),
            ('Kecamatan Darul Imarah', 'Kecamatan Darul Imarah'),
            ('Kecamatan Darul Kamal', 'Kecamatan Darul Kamal'),
            ('Kecamatan Darussalam', 'Kecamatan Darussalam'),
            ('Kecamatan Indrapuri', 'Kecamatan Indrapuri'),
            ('Kecamatan Ingin Jaya', 'Kecamatan Ingin Jaya'),
            ('Kecamatan Kota Cot Glie', 'Kecamatan Kota Cot Glie'),
            ('Kecamatan Kota Jantho', 'Kecamatan Kota Jantho'),
            ('Kecamatan Krueng Barona Jaya', 'Kecamatan Krueng Barona Jaya'),
            ('Kecamatan Kuta Baro', 'Kecamatan Kuta Baro'),
            ('Kecamatan Kuta Malaka', 'Kecamatan Kuta Malaka'),
            ('Kecamatan Lembah Seulawah', 'Kecamatan Lembah Seulawah'),
            ('Kecamatan Leupung', 'Kecamatan Leupung'),
            ('Kecamatan Lhoknga', 'Kecamatan Lhoknga'),
            ('Kecamatan Lhoong', 'Kecamatan Lhoong'),
            ('Kecamatan Mesjid Raya', 'Kecamatan Mesjid Raya'),
            ('Kecamatan Montasik', 'Kecamatan Montasik'),
            ('Kecamatan Peukan Bada', 'Kecamatan Peukan Bada'),
            ('Kecamatan Pulo Aceh', 'Kecamatan Pulo Aceh'),
            ('Kecamatan Seulimum', 'Kecamatan Seulimum'),
            ('Kecamatan Simpang Tiga', 'Kecamatan Simpang Tiga'),
            ('Kecamatan Suka Makmur', 'Kecamatan Suka Makmur'),
        ],        
        'Kabupaten Aceh Jaya': [
            ('Kecamatan Darul Hikmah', 'Kecamatan Darul Hikmah'),
            ('Kecamatan Indra Jaya', 'Kecamatan Indra Jaya'),
            ('Kecamatan Jaya', 'Kecamatan Jaya'),
            ('Kecamatan Krueng Sabee', 'Kecamatan Krueng Sabee'),
            ('Kecamatan Panga', 'Kecamatan Panga'),
            ('Kecamatan Pasie Raya', 'Kecamatan Pasie Raya'),
            ('Kecamatan Sampoiniet', 'Kecamatan Sampoiniet'),
            ('Kecamatan Setia Bakti', 'Kecamatan Setia Bakti'),
            ('Kecamatan Teunom', 'Kecamatan Teunom'),
        ],        
        'Kabupaten Aceh Selatan': [
            ('Kecamatan Bakongan', 'Kecamatan Bakongan'),
            ('Kecamatan Bakongan Timur', 'Kecamatan Bakongan Timur'),
            ('Kecamatan Kluet Selatan', 'Kecamatan Kluet Selatan'),
            ('Kecamatan Kluet Tengah', 'Kecamatan Kluet Tengah'),
            ('Kecamatan Kluet Timur', 'Kecamatan Kluet Timur'),
            ('Kecamatan Kluet Utara', 'Kecamatan Kluet Utara'),
            ('Kecamatan Kota Bahagia', 'Kecamatan Kota Bahagia'),
            ('Kecamatan Labuhan Haji', 'Kecamatan Labuhan Haji'),
            ('Kecamatan Labuhan Haji Barat', 'Kecamatan Labuhan Haji Barat'),
            ('Kecamatan Labuhan Haji Timur', 'Kecamatan Labuhan Haji Timur'),
            ('Kecamatan Meukek', 'Kecamatan Meukek'),
            ('Kecamatan Pasie Raja', 'Kecamatan Pasie Raja'),
            ('Kecamatan Samadua', 'Kecamatan Samadua'),
            ('Kecamatan Sawang', 'Kecamatan Sawang'),
            ('Kecamatan Tapak Tuan', 'Kecamatan Tapak Tuan'),
            ('Kecamatan Trumon', 'Kecamatan Trumon'),
            ('Kecamatan Trumon Tengah', 'Kecamatan Trumon Tengah'),
            ('Kecamatan Trumon Timur', 'Kecamatan Trumon Timur'),
        ],        
        'Kabupaten Aceh Singkil': [
            ('Kecamatan Danau Paris', 'Kecamatan Danau Paris'),
            ('Kecamatan Gunung Meriah', 'Kecamatan Gunung Meriah'),
            ('Kecamatan Kota Baharu', 'Kecamatan Kota Baharu'),
            ('Kecamatan Kuala Baru', 'Kecamatan Kuala Baru'),
            ('Kecamatan Pulau Banyak', 'Kecamatan Pulau Banyak'),
            ('Kecamatan Pulau Banyak Barat', 'Kecamatan Pulau Banyak Barat'),
            ('Kecamatan Simpang Kanan', 'Kecamatan Simpang Kanan'),
            ('Kecamatan Singkil', 'Kecamatan Singkil'),
            ('Kecamatan Singkil Utara', 'Kecamatan Singkil Utara'),
            ('Kecamatan Singkohor', 'Kecamatan Singkohor'),
            ('Kecamatan Suro Makmur', 'Kecamatan Suro Makmur'),
        ],        
        'Kabupaten Aceh Tamiang': [
            ('Kecamatan Banda Mulia', 'Kecamatan Banda Mulia'),
            ('Kecamatan Bandar Pusaka', 'Kecamatan bandar Pusaka'),
            ('Kecamatan Bendahara', 'Kecamatan Bendahara'),
            ('Kecamatan Karang Baru', 'Kecamatan Karang Baru'),
            ('Kecamatan Kejuruan Muda', 'Kecamatan Kejuruan Muda'),
            ('Kecamatan Kuala Simpang', 'Kecamatan Kuala Simpang'),
            ('Kecamatan Manyak Payed', 'Kecamatan Manyak Payed'),
            ('Kecamatan Rantau', 'Kecamatan Rantau'),
            ('Kecamatan Sekerak', 'Kecamatan Sekerak'),
            ('Kecamatan Seruway', 'Kecamatan Seruway'),
            ('Kecamatan Tamiang Hulu', 'Kecamatan Tamiang Hulu'),
            ('Kecamatan Tenggulun', 'Kecamatan Tenggulun'),
        ],        
        'Kabupaten Aceh Tengah': [
            ('Kecamatan Alu Lintang', 'Kecamatan Alu Lintang'),
            ('Kecamatan Bebesen', 'Kecamatan Bebesen'),
            ('Kecamatan Bies', 'Kecamatan Bies'),
            ('Kecamatan Bintang', 'Kecamatan Bintang'),
            ('Kecamatan Celala', 'Kecamatan Celala'),
            ('Kecamatan Jagong Jeget', 'Kecamatan Jagong Jeget'),
            ('Kecamatan Kebayakan', 'Kecamatan Kebayakan'),
            ('Kecamatan Ketol', 'Kecamatan Ketol'),
            ('Kecamatan Kute Panang', 'Kecamatan Kute Panang'),
            ('Kecamatan Laut Tawar', 'Kecamatan Laut Tawar'),
            ('Kecamatan Linge', 'Kecamatan Linge'),
            ('Kecamatan Peugasing', 'Kecamatan Peugasing'),
            ('Kecamatan Rusi Pantara', 'Kecamatan Rusi Pantara'),
            ('Kecamatan Silih Nara', 'Kecamatan Silih Nara'),
        ],        
        'Kabupaten Aceh Tenggara': [
            ('Kecamatan Babul Makmur', 'Kecamatan Babul Makmur'),
            ('Kecamatan Babul Rahmah', 'Kecamatan Babul Rahmah'),
            ('Kecamatan Babussalam', 'Kecamatan Babussalam'),
            ('Kecamatan Badar', 'Kecamatan Badar'),
            ('Kecamatan Bambel', 'Kecamatan Bambel'),
            ('Kecamatan Bukit Tusam', 'Kecamatan Bukit Tusam'),
            ('Kecamatan Darul Hasanah', 'Kecamatan Darul Hasanah'),
            ('Kecamatan Deleng Pokhisen', 'Kecamatan Deleng Pokhisen'),
            ('Kecamatan Ketambe', 'Kecamatan Ketambe'),
            ('Kecamatan Lawe Alas', 'Kecamatan Lawe Alas'),
            ('Kecamatan Lawe Bulan', 'Kecamatan Lawe Bulan'),
            ('Kecamatan Lawe Sigala Gala', 'Kecamatan Lawe Sigala Gala'),
            ('Kecamatan Lawe Sumur', 'Kecamatan Lawe Sumur'),
            ('Kecamatan Leuser', 'Kecamatan Leuser'),
            ('Kecamatan Semadam', 'Kecamatan Semadam'),
            ('Kecamatan Tanoh Alas', 'Kecamatan Tanoh Alas'),
        ],        
        'Kabupaten Aceh Timur': [
            ('Kecamatan Banda Alam', 'Kecamatan Banda Alam'),
            ('Kecamatan Birem Bayeun', 'Kecamatan Birem Bayeun'),
            ('Kecamatan Darul Aman', 'Kecamatan Darul Aman'),
            ('Kecamatan Darul Falah', 'Kecamatan Darul Falah'),
            ('Kecamatan Darul Ihsan', 'Kecamatan Darul Ihsan'),
            ('Kecamatan Idi Rayeuk', 'Kecamatan Idi Rayeuk'),
            ('Kecamatan Idi Timur', 'Kecamatan Idi Timur'),
            ('Kecamatan Idi Tunong', 'Kecamatan Idi Tunong'),
            ('Kecamatan Indra Makmur', 'Kecamatan Indra Makmur'),
            ('Kecamatan Julok', 'Kecamatan Julok'),
            ('Kecamatan Madat', 'Kecamatan Madat'),
            ('Kecamatan Nurussalam', 'Kecamatan Nurussalam'),
            ('Kecamatan Pante Bidari', 'Kecamatan Pante Bidari'),
            ('Kecamatan Peudawa', 'Kecamatan Peudawa'),
            ('Kecamatan Peunaron', 'Kecamatan Peunaron'),
            ('Kecamatan Peureulak', 'Kecamatan Peureulak'),
            ('Kecamatan Peureulak Barat', 'Kecamatan Peureulak Barat'),
            ('Kecamatan Peureulak Timur', 'Kecamatan Peureulak Timur'),
            ('Kecamatan Rantau Peureulak', 'Kecamatan Rantau Peureulak'),
            ('Kecamatan Rantau Selamat', 'Kecamatan Rantau Selamat'),
            ('Kecamatan Serba Jadi', 'Kecamatan Serba Jadi'),
            ('Kecamatan Simpang Jernih', 'Kecamatan Simpang Jernih'),
            ('Kecamatan Simpang Ulim', 'Kecamatan Simpang Ulim'),
            ('Kecamatan Sungai Raya', 'Kecamatan Sungai Raya'),
        ],        
        'Kabupaten Aceh Utara': [
            ('Kecamatan Baktiya', 'Kecamatan Baktiya'),
            ('Kecamatan Baktiya Barat', 'Kecamatan Baktiya Barat'),
            ('Kecamatan Bandar Baro', 'Kecamatan Bandar Baro'),
            ('Kecamatan Cot Girek', 'Kecamatan Cot Girek'),
            ('Kecamatan Dewantara', 'Kecamatan Dewantara'),
            ('Kecamatan Geureudong Pase', 'Kecamatan Geureudong Pase'),
            ('Kecamatan Kuta Makmur', 'Kecamatan Kuta Makmur'),
            ('Kecamatan Langkahan', 'Kecamatan Langkahan'),
            ('Kecamatan Lapang', 'Kecamatan Lapang'),
            ('Kecamatan Lhoksukon', 'Kecamatan Lhoksukon'),
            ('Kecamatan Matangkuli', 'Kecamatan Matangkuli'),
            ('Kecamatan Meurah Mulia', 'Kecamatan Meurah Mulia'),
            ('Kecamatan Muara Batu', 'Kecamatan Muara Batu'),
            ('Kecamatan Nibong', 'Kecamatan Nibong'),
            ('Kecamatan Nisam', 'Kecamatan Nisam'),
            ('Kecamatan Nisam Antara', 'Kecamatan Nisam Antara'),
            ('Kecamatan Paya Bakong', 'Kecamatan Paya Bakong'),
            ('Kecamatan Pirak Timur', 'Kecamatan Pirak Timur'),
            ('Kecamatan Samudera', 'Kecamatan Samudera'),
            ('Kecamatan kecamatansawangacehutara', 'Kecamatan kecamatansawangacehutara'),
            ('Kecamatan Seunuddon', 'Kecamatan Seunuddon'),
            ('Kecamatan Simpang Kramat', 'Kecamatan Simpang Kramat'),
            ('Kecamatan Syamtalira Aron', 'Kecamatan Syamtalira Aron'),
            ('Kecamatan Syamtalira Bayu', 'Kecamatan Syamtalira Bayu'),
            ('Kecamatan Tanah Luas', 'Kecamatan Tanah Luas'),
            ('Kecamatan Tanah Pasir', 'Kecamatan Tanah Pasir'),
            ('Kecamatan Tjambo Aye', 'Kecamatan Tjambo Aye'),
        ],        
        'Kabupaten Bener Meriah': [
            ('Kecamatan Bandar', 'Kecamatan Bandar'),
            ('Kecamatan Bener Kelipah', 'Kecamatan Bener Kelipah'),
            ('Kecamatan Bukit', 'Kecamatan Bukit'),
            ('Kecamatan Gajah Putih', 'Kecamatan Gajah Putih'),
            ('Kecamatan Mesidah', 'Kecamatan Mesidah'),
            ('Kecamatan Permata', 'Kecamatan Permata'),
            ('Kecamatan Pintu Rime Gayo', 'Kecamatan Pintu Rime Gayo'),
            ('Kecamatan Syiah Utama', 'Kecamatan Syiah Utama'),
            ('Kecamatan Timang Gajah', 'Kecamatan Timang Gajah'),
            ('Kecamatan Wih Pesam', 'Kecamatan Wih Pesam'),
        ],       
        'Kabupaten Bireuen': [
            ('Kecamatan Gandapura', 'Kecamatan Gandapura'),
            ('Kecamatan Jangka', 'Kecamatan Jangka'),
            ('Kecamatan Jeumpa', 'Kecamatan Jeumpa'),
            ('Kecamatan Jeunieb', 'Kecamatan Jeunieb'),
            ('Kecamatan Juli', 'Kecamatan Juli'),
            ('Kecamatan Kota Juang', 'Kecamatan Kota Juang'),
            ('Kecamatan Kuala', 'Kecamatan Kuala'),
            ('Kecamatan Kuta Blang', 'Kecamatan Kuta Blang'),
            ('Kecamatan Makmur', 'Kecamatan Makmur'),
            ('Kecamatan Pandrah', 'Kecamatan Pandrah'),
            ('Kecamatan Peudada', 'Kecamatan Peudada'),
            ('Kecamatan Peulimbang', 'Kecamatan Peulimbang'),
            ('Kecamatan Peusangan', 'Kecamatan Peusangan'),
            ('Kecamatan Peusangan Selatan', 'Kecamatan Peusangan Selatan'),
            ('Kecamatan Peusangan Siblah Krueng', 'Kecamatan Peusangan Siblah Krueng'),
            ('Kecamatan Samalanga', 'Kecamatan Samalanga'),
            ('Kecamatan Simpang Mamplam', 'Kecamatan SImpang Mamplam'),
        ],        
        'Kabupaten Gayo Lues': [
            ('Kecamatan Blang Jerango', 'Kecamatan Blang Jerango'),
            ('Kecamatan Blangkejeren', 'Kecamatan Blangkejeren'),
            ('Kecamatan Blang Pegayon', 'Kecamatan Blang Pegayon'),
            ('Kecamatan Dabun Gelang', 'Kecamatan Dabun Gelang'),
            ('Kecamatan Kutapanjang', 'Kecamatan Kutapanjang'),
            ('Kecamatan Pantan Cuaca', 'Kecamatan Pantan Cuaca'),
            ('Kecamatan Pining', 'Kecamatan Pining'),
            ('Kecamatan Puteri Betung', 'Kecamatan Puteri Betung'),
            ('Kecamatan Rikit Gaib', 'Kecamatan Rikit Gaib'),
            ('Kecamatan terangun', 'Kecamatan Terangun'),
            ('Kecamatan Teripe Jaya', 'Kecamatan Teripe Jaya'),
        ],        
        'Kabupaten Nagan Raya': [
            ('Kecamatan Beutong', 'Kecamatan Beutong'),
            ('Kecamatan Beutong Ateuh', 'Kecamatan Beutong Ateuh'),
            ('Kecamatan Darul Makmur', 'Kecamatan Darul Makmur'),
            ('Kecamatan Kuala Nagan', 'Kecamatan Kuala Nagan'),
            ('Kecamatan Kuala Pesisir', 'Kecamatan Kuala Pesisir'),
            ('Kecamatan Seunangan', 'Kecamatan Seunangan'),
            ('Kecamatan Seunangan Timur', 'Kecamatan Seunangan Timur'),
            ('Kecamatan Suka Makmue', 'Kecamatan Suka Makmue'),
            ('Kecamatan Tadu Raya', 'Kecamatan Tadu Raya'),
            ('Kecamatan Tripa Makmur', 'Kecamatan Tripa Makmur'),
        ],        
        'Kabupaten Pidie': [
            ('Kecamatan Batee', 'Kecamatan Batee'),
            ('Kecamatan Delima', 'Kecamatan Delima'),
            ('Kecamatan Geulumpang Tiga', 'Kecamatan Geulumpang Tiga'),
            ('Kecamatan Geumpang', 'Kecamatan Geumpang'),
            ('Kecamatan Glumpang Baro', 'Kecamatan Glumpang Baro'),
            ('Kecamatan Grong Grong', 'Kecamatan Grong Grong'),
            ('Kecamatan Indra Jaya', 'Kecamatan Indra Jaya'),
            ('Kecamatan Kembang Tanjong', 'Kecamatan Kembang Tanjong'),
            ('Kecamatan Keumala', 'Kecamatan Keumala'),
            ('Kecamatan Kota Sigli', 'Kecamatan Kota Sigli'),
            ('Kecamatan Mane', 'Kecamatan Mane'),
            ('Kecamatan Mila', 'Kecamatan Mila'),
            ('Kecamatan Muara Tiga', 'Kecamatan Muara Tiga'),
            ('Kecamatan Mutiara', 'Kecamatan Mutiara'),
            ('Kecamatan Mutiara Timur', 'Kecamatan Mutiara Timur'),
            ('Kecamatan Padang Tiji', 'Kecamatan Padang Tiji'),
            ('Kecamatan Peukan Baro', 'Kecamatan Peukan Baro'),
            ('Kecamatan Pidie', 'Kecamatan Pidie'),
            ('Kecamatan Sakti', 'Kecamatan Sakti'),
            ('Kecamatan Simpang Tiga', 'Kecamatan Simpang Tiga'),
            ('Kecamatan Tangse', 'Kecamatan Tangse'),
            ('Kecamatan Tiro', 'Kecamatan Tiro'),
            ('Kecamatan Titeue', 'Kecamatan Titeue'),
        ],        
        'Kabupaten Pidie Jaya': [
            ('Kecamatan Bandar Dua', 'Kecamatan Bandar Dua'),
            ('Kecamatan Bandar Baru', 'Kecamatan Bandar Baru'),
            ('Kecamatan Jangka Buya', 'Kecamatan Jangka Buya'),
            ('Kecamatan Meurah Dua', 'Kecamatan Meurah Dua'),
            ('Kecamatan Meureudu', 'Kecamatan Meureudu'),
            ('Kecamatan Panteraja', 'Kecamatan Panteraja'),
            ('Kecamatan Trienggadeng', 'Kecamatan Trienggadeng'),
            ('Kecamatan Ulim', 'Kecamatan Ulim'),
        ],        
        'Kabupaten Simeulue': [
            ('Kecamatan Alapan', 'Kecamatan Alapan'),
            ('Kecamatan Salang', 'Kecamatan Salang'),
            ('Kecamatan Simeulue Barat', 'Kecamatan Simeulue Barat'),
            ('Kecamatan Simeulue Cut', 'Kecamatan Simeulue Cut'),
            ('Kecamatan Simeulue Tengah', 'Kecamatan Simeulue Tengah'),
            ('Kecamatan Simeulue Timur', 'Kecamatan Simeulue Timur'),
            ('Kecamatan Teluk Dalam', 'Kecamatan Teluk Dalam'),
            ('Kecamatan Teupah Barat', 'Kecamatan Teupah Barat'),
            ('Kecamatan Teupah Selatan', 'Kecamatan Teupah Selatan'),
            ('Kecamatan Teupah Tengah', 'Kecamatan Teupah Tengah'),
        ],        
        'Kota Banda Aceh': [
            ('Kecamatan Baiturrahman', 'Kecamatan Baiturrahman'),
            ('Kecamatan Bandar Raya', 'Kecamatan Bandar Raya'),
            ('Kecamatan Jaya Baru', 'Kecamatan Jaya Baru'),
            ('Kecamatan Kuta Alam', 'Kecamatan Kuta Alam'),
            ('Kecamatan Kuta Raja', 'Kecamatan Kuta Raja'),
            ('Kecamatan Lueng Bata', 'Kecamatan Lueng Bata'),
            ('Kecamatan Meuraxa', 'Kecamatan Meuraxa'),
            ('Kecamatan Syiah Kuala', 'Kecamatan Syiah Kuala'),
            ('Kecamatan Ulee Kareng', 'Kecamatan Ulee Kareng'),
        ],        
        'Kota Langsa': [
            ('Kecamatan Langsa Barat', 'Kecamatan Langsa Barat'),
            ('Kecamatan Langsa Baro', 'Kecamatan Langsa Baro'),
            ('Kecamatan Langsa Kota', 'Kecamatan Langsa Kota'),
            ('Kecamatan Langsa Lama', 'Kecamatan Langsa Lama'),
            ('Kecamatan Langsa Timur', 'Kecamatan Langsa Timur'),
        ],        
        'Kota Lhokseumawe': [
            ('Kecamatan Banda Sakti', 'Kecamatan Banda Sakti'),
            ('Kecamatan Blang Mangat', 'Kecamatan Blang Mangat'),
            ('Kecamatan Muara Dua', 'Kecamatan Muara Dua'),
            ('Kecamatan Muara Satu', 'Kecamatan Muara Satu'),
        ],        
        'Kota Sabang': [
            ('Kecamatan Sukajaya', 'Kecamatan Sukajaya'),
            ('Kecamatan Sukakarya', 'Kecamatan Sukakarya'),
            ('Kecamatan Sukamakmue', 'Kecamatan Sukamakmue'),
        ],        
        'Kota Subulussalam': [
            ('Kecamatan Longkib', 'Kecamatan Longkib'),
            ('Kecamatan Penanggalan', 'Kecamatan Penanggalan'),
            ('Kecamatan Rundeng', 'Kecamatan Rundeng'),
            ('Kecamatan Simpang Kiri', 'Kecamatan Simpang Kiri'),
            ('Kecamatan Sultan Daulat', 'Kecamatan Sultan Daulat'),
        ],    
    }
    
    AKREDITASI_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('TT', 'TT'),
    )
    
    JENJANG_CHOICES = [
        ('SMA', 'SMA'),
        ('SMK', 'SMK'),
    ]
    
    SEKOLAH_CHOICES = [
        ('Negeri', 'Negeri'),
        ('Swasta', 'Swasta'),
    ]
    
    STATUS_CHOICES = [
        ('Menunggu', 'Menunggu'),
        ('Ditolak', 'Ditolak'),
        ('Disetujui', 'Disetujui'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    NPSN = models.BigIntegerField()
    NamaSekolah = models.CharField(max_length=250)
    NamaKepalaSekolah = models.CharField(max_length=250)
    NamaPengawasSekolah = models.CharField(max_length=250)
    AlamatSekolah = models.CharField(max_length=600)
    JumlahGuru = models.BigIntegerField()
    JumlahKelas = models.BigIntegerField()
    JenjangSekolah = models.CharField(max_length=50, choices=JENJANG_CHOICES)
    StatusSekolah = models.CharField(max_length=50, choices=SEKOLAH_CHOICES)
    KabupatenKota = models.CharField(max_length=600, choices=KABUPATENKOTA_CHOICES)
    Kecamatan = models.CharField(max_length=250)
    AkreditasiSekolah = models.CharField(max_length=50, choices=AKREDITASI_CHOICES)
    TahunPengajuanTerakhir = models.IntegerField()
    TanggalAjukan = models.DateField(auto_now_add=True, null=True, blank=True)
    StatusPengajuan = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Menunggu',
    )
    

class TemporaryPolygon(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    SekolahId = models.ForeignKey(TemporaryPengajuanSekolah, on_delete=models.CASCADE)
    geometri = JSONField()
    warna = models.CharField(max_length=20, null=True, blank=True)
    
def warna_akreditasi(akreditasi):
        if akreditasi == 'A':
            return 'green'
        elif akreditasi == 'B':
            return 'blue'
        elif akreditasi == 'C':
            return 'yellow'
        elif akreditasi == 'TT':
            return 'red'
        else:
            return 'gray'

class PengajuanSekolahModel(models.Model):
    
    KABUPATENKOTA_CHOICES = [
        ('Kabupaten Aceh Barat','Kabupaten Aceh Barat'),
        ('Kabupaten Aceh Barat Daya','Kabupaten Aceh Barat Daya'),
        ('Kabupaten Aceh Besar','Kabupaten Aceh Besar'),
        ('Kabupaten Aceh Jaya','Kabupaten Aceh Jaya'),
        ('Kabupaten Aceh Selatan','Kabupaten Aceh Selatan'),
        ('Kabupaten Aceh Singkil','Kabupaten Aceh Singkil'),
        ('Kabupaten Aceh Tamiang','Kabupaten Aceh Tamiang'),
        ('Kabupaten Aceh Tengah','Kabupaten Aceh Tengah'),
        ('Kabupaten Aceh Tenggara','Kabupaten Aceh Tenggara'),
        ('Kabupaten Aceh Timur','Kabupaten Aceh Timur'),
        ('Kabupaten Aceh Utara','Kabupaten Aceh Utara'),
        ('Kabupaten Bener Meriah','Kabupaten Bener Meriah'),
        ('Kabupaten Bireun','Kabupaten Bireun'),
        ('Kabupaten Gayo Lues','Kabupaten Gayo Lues'),
        ('Kabupaten Nagan Raya','Kabupaten Nagan Raya'),
        ('Kabupaten Pidie','Kabupaten Pidie'),
        ('Kabupaten Pidie Jaya','Kabupaten Pidie Jaya'),
        ('Kabupaten Simeulue','Kabupaten Simeulue'),
        ('Kota Banda Aceh','Kota Banda Aceh'),
        ('Kota Langsa','Kota Langsa'),
        ('Kota Lhokseumawe','Kota Lhokseumawe'),
        ('Kota Sabang','Kota Sabang'),
        ('Kota Subulussalam','Kota Subulussalam'),
    ]
    
    KECAMATAN_CHOICES = {
        'Kabupaten Aceh Barat': [
            ('Kecamatan Arongan Lambalek', 'Kecamatan Arongan Lambalek'),
            ('Kecamatan Bubon', 'Kecamatan Bubon'),
            ('Kecamatan Johan Pahlawan', 'Kecamatan Johan Pahlawan'),
            ('Kecamatan Kaway XVI', 'Kecamatan Kaway XVI'),
            ('Kecamatan Meureubo', 'Kecamatan Meureubo'),
            ('Kecamatan Pante Ceureumen', 'Kecamatan Pante Ceureumen'),
            ('Kecamatan Panton reu', 'Kecamatan Panton reu'),
            ('Kecamatan Samatiga', 'Kecamatan Samatiga'),
            ('Kecamatan Sungai Mas', 'Kecamatan Sungai Mas'),
            ('Kecamatan Woyla', 'Kecamatan Woyla'),
            ('Kecamatan Woyla Barat', 'Kecamatan Woyla Barat'),
            ('Kecamatan Woyla Timur', 'Kecamatan Woyla Timur'),
        ],
        'Kabupaten Aceh Barat Daya': [
            ('Kecamatan Babahrot', 'Kecamatan Babahrot'),
            ('Kecamatan Blang Pidie', 'Kecamatan Blang Pidie'),
            ('Kecamatan Jeumpa', 'Kecamatan Jeumpa'),
            ('Kecamatan Kuala Batee', 'Kecamatan Kuala Batee'),
            ('Kecamatan Lembah Sabil', 'Kecamatan Lembah Sabil'),
            ('Kecamatan Manggeng', 'Kecamatan Manggeng'),
            ('Kecamatan Setia', 'Kecamatan Setia'),
            ('Kecamatan Susoh', 'Kecamatan Susoh'),
            ('Kecamatan Tangan Tangan', 'Kecamatan Tangan Tangan'),
        ],
        'Kabupaten Aceh Besar': [
            ('Kecamatan Baitussalam', 'Kecamatan Baitussalam'),
            ('Kecamatan Blang Bintang', 'Kecamatan Blang Bintang'),
            ('Kecamatan Darul Imarah', 'Kecamatan Darul Imarah'),
            ('Kecamatan Darul Kamal', 'Kecamatan Darul Kamal'),
            ('Kecamatan Darussalam', 'Kecamatan Darussalam'),
            ('Kecamatan Indrapuri', 'Kecamatan Indrapuri'),
            ('Kecamatan Ingin Jaya', 'Kecamatan Ingin Jaya'),
            ('Kecamatan Kota Cot Glie', 'Kecamatan Kota Cot Glie'),
            ('Kecamatan Kota Jantho', 'Kecamatan Kota Jantho'),
            ('Kecamatan Krueng Barona Jaya', 'Kecamatan Krueng Barona Jaya'),
            ('Kecamatan Kuta Baro', 'Kecamatan Kuta Baro'),
            ('Kecamatan Kuta Malaka', 'Kecamatan Kuta Malaka'),
            ('Kecamatan Lembah Seulawah', 'Kecamatan Lembah Seulawah'),
            ('Kecamatan Leupung', 'Kecamatan Leupung'),
            ('Kecamatan Lhoknga', 'Kecamatan Lhoknga'),
            ('Kecamatan Lhoong', 'Kecamatan Lhoong'),
            ('Kecamatan Mesjid Raya', 'Kecamatan Mesjid Raya'),
            ('Kecamatan Montasik', 'Kecamatan Montasik'),
            ('Kecamatan Peukan Bada', 'Kecamatan Peukan Bada'),
            ('Kecamatan Pulo Aceh', 'Kecamatan Pulo Aceh'),
            ('Kecamatan Seulimum', 'Kecamatan Seulimum'),
            ('Kecamatan Simpang Tiga', 'Kecamatan Simpang Tiga'),
            ('Kecamatan Suka Makmur', 'Kecamatan Suka Makmur'),
        ],        
        'Kabupaten Aceh Jaya': [
            ('Kecamatan Darul Hikmah', 'Kecamatan Darul Hikmah'),
            ('Kecamatan Indra Jaya', 'Kecamatan Indra Jaya'),
            ('Kecamatan Jaya', 'Kecamatan Jaya'),
            ('Kecamatan Krueng Sabee', 'Kecamatan Krueng Sabee'),
            ('Kecamatan Panga', 'Kecamatan Panga'),
            ('Kecamatan Pasie Raya', 'Kecamatan Pasie Raya'),
            ('Kecamatan Sampoiniet', 'Kecamatan Sampoiniet'),
            ('Kecamatan Setia Bakti', 'Kecamatan Setia Bakti'),
            ('Kecamatan Teunom', 'Kecamatan Teunom'),
        ],        
        'Kabupaten Aceh Selatan': [
            ('Kecamatan Bakongan', 'Kecamatan Bakongan'),
            ('Kecamatan Bakongan Timur', 'Kecamatan Bakongan Timur'),
            ('Kecamatan Kluet Selatan', 'Kecamatan Kluet Selatan'),
            ('Kecamatan Kluet Tengah', 'Kecamatan Kluet Tengah'),
            ('Kecamatan Kluet Timur', 'Kecamatan Kluet Timur'),
            ('Kecamatan Kluet Utara', 'Kecamatan Kluet Utara'),
            ('Kecamatan Kota Bahagia', 'Kecamatan Kota Bahagia'),
            ('Kecamatan Labuhan Haji', 'Kecamatan Labuhan Haji'),
            ('Kecamatan Labuhan Haji Barat', 'Kecamatan Labuhan Haji Barat'),
            ('Kecamatan Labuhan Haji Timur', 'Kecamatan Labuhan Haji Timur'),
            ('Kecamatan Meukek', 'Kecamatan Meukek'),
            ('Kecamatan Pasie Raja', 'Kecamatan Pasie Raja'),
            ('Kecamatan Samadua', 'Kecamatan Samadua'),
            ('Kecamatan Sawang', 'Kecamatan Sawang'),
            ('Kecamatan Tapak Tuan', 'Kecamatan Tapak Tuan'),
            ('Kecamatan Trumon', 'Kecamatan Trumon'),
            ('Kecamatan Trumon Tengah', 'Kecamatan Trumon Tengah'),
            ('Kecamatan Trumon Timur', 'Kecamatan Trumon Timur'),
        ],        
        'Kabupaten Aceh Singkil': [
            ('Kecamatan Danau Paris', 'Kecamatan Danau Paris'),
            ('Kecamatan Gunung Meriah', 'Kecamatan Gunung Meriah'),
            ('Kecamatan Kota Baharu', 'Kecamatan Kota Baharu'),
            ('Kecamatan Kuala Baru', 'Kecamatan Kuala Baru'),
            ('Kecamatan Pulau Banyak', 'Kecamatan Pulau Banyak'),
            ('Kecamatan Pulau Banyak Barat', 'Kecamatan Pulau Banyak Barat'),
            ('Kecamatan Simpang Kanan', 'Kecamatan Simpang Kanan'),
            ('Kecamatan Singkil', 'Kecamatan Singkil'),
            ('Kecamatan Singkil Utara', 'Kecamatan Singkil Utara'),
            ('Kecamatan Singkohor', 'Kecamatan Singkohor'),
            ('Kecamatan Suro Makmur', 'Kecamatan Suro Makmur'),
        ],        
        'Kabupaten Aceh Tamiang': [
            ('Kecamatan Banda Mulia', 'Kecamatan Banda Mulia'),
            ('Kecamatan Bandar Pusaka', 'Kecamatan bandar Pusaka'),
            ('Kecamatan Bendahara', 'Kecamatan Bendahara'),
            ('Kecamatan Karang Baru', 'Kecamatan Karang Baru'),
            ('Kecamatan Kejuruan Muda', 'Kecamatan Kejuruan Muda'),
            ('Kecamatan Kuala Simpang', 'Kecamatan Kuala Simpang'),
            ('Kecamatan Manyak Payed', 'Kecamatan Manyak Payed'),
            ('Kecamatan Rantau', 'Kecamatan Rantau'),
            ('Kecamatan Sekerak', 'Kecamatan Sekerak'),
            ('Kecamatan Seruway', 'Kecamatan Seruway'),
            ('Kecamatan Tamiang Hulu', 'Kecamatan Tamiang Hulu'),
            ('Kecamatan Tenggulun', 'Kecamatan Tenggulun'),
        ],        
        'Kabupaten Aceh Tengah': [
            ('Kecamatan Alu Lintang', 'Kecamatan Alu Lintang'),
            ('Kecamatan Bebesen', 'Kecamatan Bebesen'),
            ('Kecamatan Bies', 'Kecamatan Bies'),
            ('Kecamatan Bintang', 'Kecamatan Bintang'),
            ('Kecamatan Celala', 'Kecamatan Celala'),
            ('Kecamatan Jagong Jeget', 'Kecamatan Jagong Jeget'),
            ('Kecamatan Kebayakan', 'Kecamatan Kebayakan'),
            ('Kecamatan Ketol', 'Kecamatan Ketol'),
            ('Kecamatan Kute Panang', 'Kecamatan Kute Panang'),
            ('Kecamatan Laut Tawar', 'Kecamatan Laut Tawar'),
            ('Kecamatan Linge', 'Kecamatan Linge'),
            ('Kecamatan Peugasing', 'Kecamatan Peugasing'),
            ('Kecamatan Rusi Pantara', 'Kecamatan Rusi Pantara'),
            ('Kecamatan Silih Nara', 'Kecamatan Silih Nara'),
        ],        
        'Kabupaten Aceh Tenggara': [
            ('Kecamatan Babul Makmur', 'Kecamatan Babul Makmur'),
            ('Kecamatan Babul Rahmah', 'Kecamatan Babul Rahmah'),
            ('Kecamatan Babussalam', 'Kecamatan Babussalam'),
            ('Kecamatan Badar', 'Kecamatan Badar'),
            ('Kecamatan Bambel', 'Kecamatan Bambel'),
            ('Kecamatan Bukit Tusam', 'Kecamatan Bukit Tusam'),
            ('Kecamatan Darul Hasanah', 'Kecamatan Darul Hasanah'),
            ('Kecamatan Deleng Pokhisen', 'Kecamatan Deleng Pokhisen'),
            ('Kecamatan Ketambe', 'Kecamatan Ketambe'),
            ('Kecamatan Lawe Alas', 'Kecamatan Lawe Alas'),
            ('Kecamatan Lawe Bulan', 'Kecamatan Lawe Bulan'),
            ('Kecamatan Lawe Sigala Gala', 'Kecamatan Lawe Sigala Gala'),
            ('Kecamatan Lawe Sumur', 'Kecamatan Lawe Sumur'),
            ('Kecamatan Leuser', 'Kecamatan Leuser'),
            ('Kecamatan Semadam', 'Kecamatan Semadam'),
            ('Kecamatan Tanoh Alas', 'Kecamatan Tanoh Alas'),
        ],        
        'Kabupaten Aceh Timur': [
            ('Kecamatan Banda Alam', 'Kecamatan Banda Alam'),
            ('Kecamatan Birem Bayeun', 'Kecamatan Birem Bayeun'),
            ('Kecamatan Darul Aman', 'Kecamatan Darul Aman'),
            ('Kecamatan Darul Falah', 'Kecamatan Darul Falah'),
            ('Kecamatan Darul Ihsan', 'Kecamatan Darul Ihsan'),
            ('Kecamatan Idi Rayeuk', 'Kecamatan Idi Rayeuk'),
            ('Kecamatan Idi Timur', 'Kecamatan Idi Timur'),
            ('Kecamatan Idi Tunong', 'Kecamatan Idi Tunong'),
            ('Kecamatan Indra Makmur', 'Kecamatan Indra Makmur'),
            ('Kecamatan Julok', 'Kecamatan Julok'),
            ('Kecamatan Madat', 'Kecamatan Madat'),
            ('Kecamatan Nurussalam', 'Kecamatan Nurussalam'),
            ('Kecamatan Pante Bidari', 'Kecamatan Pante Bidari'),
            ('Kecamatan Peudawa', 'Kecamatan Peudawa'),
            ('Kecamatan Peunaron', 'Kecamatan Peunaron'),
            ('Kecamatan Peureulak', 'Kecamatan Peureulak'),
            ('Kecamatan Peureulak Barat', 'Kecamatan Peureulak Barat'),
            ('Kecamatan Peureulak Timur', 'Kecamatan Peureulak Timur'),
            ('Kecamatan Rantau Peureulak', 'Kecamatan Rantau Peureulak'),
            ('Kecamatan Rantau Selamat', 'Kecamatan Rantau Selamat'),
            ('Kecamatan Serba Jadi', 'Kecamatan Serba Jadi'),
            ('Kecamatan Simpang Jernih', 'Kecamatan Simpang Jernih'),
            ('Kecamatan Simpang Ulim', 'Kecamatan Simpang Ulim'),
            ('Kecamatan Sungai Raya', 'Kecamatan Sungai Raya'),
        ],        
        'Kabupaten Aceh Utara': [
            ('Kecamatan Baktiya', 'Kecamatan Baktiya'),
            ('Kecamatan Baktiya Barat', 'Kecamatan Baktiya Barat'),
            ('Kecamatan Bandar Baro', 'Kecamatan Bandar Baro'),
            ('Kecamatan Cot Girek', 'Kecamatan Cot Girek'),
            ('Kecamatan Dewantara', 'Kecamatan Dewantara'),
            ('Kecamatan Geureudong Pase', 'Kecamatan Geureudong Pase'),
            ('Kecamatan Kuta Makmur', 'Kecamatan Kuta Makmur'),
            ('Kecamatan Langkahan', 'Kecamatan Langkahan'),
            ('Kecamatan Lapang', 'Kecamatan Lapang'),
            ('Kecamatan Lhoksukon', 'Kecamatan Lhoksukon'),
            ('Kecamatan Matangkuli', 'Kecamatan Matangkuli'),
            ('Kecamatan Meurah Mulia', 'Kecamatan Meurah Mulia'),
            ('Kecamatan Muara Batu', 'Kecamatan Muara Batu'),
            ('Kecamatan Nibong', 'Kecamatan Nibong'),
            ('Kecamatan Nisam', 'Kecamatan Nisam'),
            ('Kecamatan Nisam Antara', 'Kecamatan Nisam Antara'),
            ('Kecamatan Paya Bakong', 'Kecamatan Paya Bakong'),
            ('Kecamatan Pirak Timur', 'Kecamatan Pirak Timur'),
            ('Kecamatan Samudera', 'Kecamatan Samudera'),
            ('Kecamatan kecamatansawangacehutara', 'Kecamatan kecamatansawangacehutara'),
            ('Kecamatan Seunuddon', 'Kecamatan Seunuddon'),
            ('Kecamatan Simpang Kramat', 'Kecamatan Simpang Kramat'),
            ('Kecamatan Syamtalira Aron', 'Kecamatan Syamtalira Aron'),
            ('Kecamatan Syamtalira Bayu', 'Kecamatan Syamtalira Bayu'),
            ('Kecamatan Tanah Luas', 'Kecamatan Tanah Luas'),
            ('Kecamatan Tanah Pasir', 'Kecamatan Tanah Pasir'),
            ('Kecamatan Tjambo Aye', 'Kecamatan Tjambo Aye'),
        ],        
        'Kabupaten Bener Meriah': [
            ('Kecamatan Bandar', 'Kecamatan Bandar'),
            ('Kecamatan Bener Kelipah', 'Kecamatan Bener Kelipah'),
            ('Kecamatan Bukit', 'Kecamatan Bukit'),
            ('Kecamatan Gajah Putih', 'Kecamatan Gajah Putih'),
            ('Kecamatan Mesidah', 'Kecamatan Mesidah'),
            ('Kecamatan Permata', 'Kecamatan Permata'),
            ('Kecamatan Pintu Rime Gayo', 'Kecamatan Pintu Rime Gayo'),
            ('Kecamatan Syiah Utama', 'Kecamatan Syiah Utama'),
            ('Kecamatan Timang Gajah', 'Kecamatan Timang Gajah'),
            ('Kecamatan Wih Pesam', 'Kecamatan Wih Pesam'),
        ],       
        'Kabupaten Bireuen': [
            ('Kecamatan Gandapura', 'Kecamatan Gandapura'),
            ('Kecamatan Jangka', 'Kecamatan Jangka'),
            ('Kecamatan Jeumpa', 'Kecamatan Jeumpa'),
            ('Kecamatan Jeunieb', 'Kecamatan Jeunieb'),
            ('Kecamatan Juli', 'Kecamatan Juli'),
            ('Kecamatan Kota Juang', 'Kecamatan Kota Juang'),
            ('Kecamatan Kuala', 'Kecamatan Kuala'),
            ('Kecamatan Kuta Blang', 'Kecamatan Kuta Blang'),
            ('Kecamatan Makmur', 'Kecamatan Makmur'),
            ('Kecamatan Pandrah', 'Kecamatan Pandrah'),
            ('Kecamatan Peudada', 'Kecamatan Peudada'),
            ('Kecamatan Peulimbang', 'Kecamatan Peulimbang'),
            ('Kecamatan Peusangan', 'Kecamatan Peusangan'),
            ('Kecamatan Peusangan Selatan', 'Kecamatan Peusangan Selatan'),
            ('Kecamatan Peusangan Siblah Krueng', 'Kecamatan Peusangan Siblah Krueng'),
            ('Kecamatan Samalanga', 'Kecamatan Samalanga'),
            ('Kecamatan Simpang Mamplam', 'Kecamatan SImpang Mamplam'),
        ],        
        'Kabupaten Gayo Lues': [
            ('Kecamatan Blang Jerango', 'Kecamatan Blang Jerango'),
            ('Kecamatan Blangkejeren', 'Kecamatan Blangkejeren'),
            ('Kecamatan Blang Pegayon', 'Kecamatan Blang Pegayon'),
            ('Kecamatan Dabun Gelang', 'Kecamatan Dabun Gelang'),
            ('Kecamatan Kutapanjang', 'Kecamatan Kutapanjang'),
            ('Kecamatan Pantan Cuaca', 'Kecamatan Pantan Cuaca'),
            ('Kecamatan Pining', 'Kecamatan Pining'),
            ('Kecamatan Puteri Betung', 'Kecamatan Puteri Betung'),
            ('Kecamatan Rikit Gaib', 'Kecamatan Rikit Gaib'),
            ('Kecamatan terangun', 'Kecamatan Terangun'),
            ('Kecamatan Teripe Jaya', 'Kecamatan Teripe Jaya'),
        ],        
        'Kabupaten Nagan Raya': [
            ('Kecamatan Beutong', 'Kecamatan Beutong'),
            ('Kecamatan Beutong Ateuh', 'Kecamatan Beutong Ateuh'),
            ('Kecamatan Darul Makmur', 'Kecamatan Darul Makmur'),
            ('Kecamatan Kuala Nagan', 'Kecamatan Kuala Nagan'),
            ('Kecamatan Kuala Pesisir', 'Kecamatan Kuala Pesisir'),
            ('Kecamatan Seunangan', 'Kecamatan Seunangan'),
            ('Kecamatan Seunangan Timur', 'Kecamatan Seunangan Timur'),
            ('Kecamatan Suka Makmue', 'Kecamatan Suka Makmue'),
            ('Kecamatan Tadu Raya', 'Kecamatan Tadu Raya'),
            ('Kecamatan Tripa Makmur', 'Kecamatan Tripa Makmur'),
        ],        
        'Kabupaten Pidie': [
            ('Kecamatan Batee', 'Kecamatan Batee'),
            ('Kecamatan Delima', 'Kecamatan Delima'),
            ('Kecamatan Geulumpang Tiga', 'Kecamatan Geulumpang Tiga'),
            ('Kecamatan Geumpang', 'Kecamatan Geumpang'),
            ('Kecamatan Glumpang Baro', 'Kecamatan Glumpang Baro'),
            ('Kecamatan Grong Grong', 'Kecamatan Grong Grong'),
            ('Kecamatan Indra Jaya', 'Kecamatan Indra Jaya'),
            ('Kecamatan Kembang Tanjong', 'Kecamatan Kembang Tanjong'),
            ('Kecamatan Keumala', 'Kecamatan Keumala'),
            ('Kecamatan Kota Sigli', 'Kecamatan Kota Sigli'),
            ('Kecamatan Mane', 'Kecamatan Mane'),
            ('Kecamatan Mila', 'Kecamatan Mila'),
            ('Kecamatan Muara Tiga', 'Kecamatan Muara Tiga'),
            ('Kecamatan Mutiara', 'Kecamatan Mutiara'),
            ('Kecamatan Mutiara Timur', 'Kecamatan Mutiara Timur'),
            ('Kecamatan Padang Tiji', 'Kecamatan Padang Tiji'),
            ('Kecamatan Peukan Baro', 'Kecamatan Peukan Baro'),
            ('Kecamatan Pidie', 'Kecamatan Pidie'),
            ('Kecamatan Sakti', 'Kecamatan Sakti'),
            ('Kecamatan Simpang Tiga', 'Kecamatan Simpang Tiga'),
            ('Kecamatan Tangse', 'Kecamatan Tangse'),
            ('Kecamatan Tiro', 'Kecamatan Tiro'),
            ('Kecamatan Titeue', 'Kecamatan Titeue'),
        ],        
        'Kabupaten Pidie Jaya': [
            ('Kecamatan Bandar Dua', 'Kecamatan Bandar Dua'),
            ('Kecamatan Bandar Baru', 'Kecamatan Bandar Baru'),
            ('Kecamatan Jangka Buya', 'Kecamatan Jangka Buya'),
            ('Kecamatan Meurah Dua', 'Kecamatan Meurah Dua'),
            ('Kecamatan Meureudu', 'Kecamatan Meureudu'),
            ('Kecamatan Panteraja', 'Kecamatan Panteraja'),
            ('Kecamatan Trienggadeng', 'Kecamatan Trienggadeng'),
            ('Kecamatan Ulim', 'Kecamatan Ulim'),
        ],        
        'Kabupaten Simeulue': [
            ('Kecamatan Alapan', 'Kecamatan Alapan'),
            ('Kecamatan Salang', 'Kecamatan Salang'),
            ('Kecamatan Simeulue Barat', 'Kecamatan Simeulue Barat'),
            ('Kecamatan Simeulue Cut', 'Kecamatan Simeulue Cut'),
            ('Kecamatan Simeulue Tengah', 'Kecamatan Simeulue Tengah'),
            ('Kecamatan Simeulue Timur', 'Kecamatan Simeulue Timur'),
            ('Kecamatan Teluk Dalam', 'Kecamatan Teluk Dalam'),
            ('Kecamatan Teupah Barat', 'Kecamatan Teupah Barat'),
            ('Kecamatan Teupah Selatan', 'Kecamatan Teupah Selatan'),
            ('Kecamatan Teupah Tengah', 'Kecamatan Teupah Tengah'),
        ],        
        'Kota Banda Aceh': [
            ('Kecamatan Baiturrahman', 'Kecamatan Baiturrahman'),
            ('Kecamatan Bandar Raya', 'Kecamatan Bandar Raya'),
            ('Kecamatan Jaya Baru', 'Kecamatan Jaya Baru'),
            ('Kecamatan Kuta Alam', 'Kecamatan Kuta Alam'),
            ('Kecamatan Kuta Raja', 'Kecamatan Kuta Raja'),
            ('Kecamatan Lueng Bata', 'Kecamatan Lueng Bata'),
            ('Kecamatan Meuraxa', 'Kecamatan Meuraxa'),
            ('Kecamatan Syiah Kuala', 'Kecamatan Syiah Kuala'),
            ('Kecamatan Ulee Kareng', 'Kecamatan Ulee Kareng'),
        ],        
        'Kota Langsa': [
            ('Kecamatan Langsa Barat', 'Kecamatan Langsa Barat'),
            ('Kecamatan Langsa Baro', 'Kecamatan Langsa Baro'),
            ('Kecamatan Langsa Kota', 'Kecamatan Langsa Kota'),
            ('Kecamatan Langsa Lama', 'Kecamatan Langsa Lama'),
            ('Kecamatan Langsa Timur', 'Kecamatan Langsa Timur'),
        ],        
        'Kota Lhokseumawe': [
            ('Kecamatan Banda Sakti', 'Kecamatan Banda Sakti'),
            ('Kecamatan Blang Mangat', 'Kecamatan Blang Mangat'),
            ('Kecamatan Muara Dua', 'Kecamatan Muara Dua'),
            ('Kecamatan Muara Satu', 'Kecamatan Muara Satu'),
        ],        
        'Kota Sabang': [
            ('Kecamatan Sukajaya', 'Kecamatan Sukajaya'),
            ('Kecamatan Sukakarya', 'Kecamatan Sukakarya'),
            ('Kecamatan Sukamakmue', 'Kecamatan Sukamakmue'),
        ],        
        'Kota Subulussalam': [
            ('Kecamatan Longkib', 'Kecamatan Longkib'),
            ('Kecamatan Penanggalan', 'Kecamatan Penanggalan'),
            ('Kecamatan Rundeng', 'Kecamatan Rundeng'),
            ('Kecamatan Simpang Kiri', 'Kecamatan Simpang Kiri'),
            ('Kecamatan Sultan Daulat', 'Kecamatan Sultan Daulat'),
        ],    
    }
    
    AKREDITASI_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('TT', 'TT'),
    )
    
    JENJANG_CHOICES = [
        ('SMA', 'SMA'),
        ('SMK', 'SMK'),
    ]
    
    SEKOLAH_CHOICES = [
        ('Negeri', 'Negeri'),
        ('Swasta', 'Swasta'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    SekolahId = models.BigAutoField(primary_key=True)
    NPSN = models.BigIntegerField()
    TanggalAjukan = models.DateField(auto_now_add=True, null=True, blank=True)
    NamaSekolah = models.CharField(max_length=250)
    NamaKepalaSekolah = models.CharField(max_length=250)
    NamaPengawasSekolah = models.CharField(max_length=250)
    AlamatSekolah = models.CharField(max_length=600)
    JumlahGuru = models.BigIntegerField()
    JumlahKelas = models.BigIntegerField()
    JenjangSekolah = models.CharField(max_length=50, choices=JENJANG_CHOICES)
    StatusSekolah = models.CharField(max_length=50, choices=SEKOLAH_CHOICES)
    KabupatenKota = models.CharField(max_length=600, choices=KABUPATENKOTA_CHOICES)
    Kecamatan = models.CharField(max_length=250)
    AkreditasiSekolah = models.CharField(max_length=50, choices=AKREDITASI_CHOICES)
    TahunPengajuanTerakhir = models.IntegerField()
    status_pengajuan = models.CharField(max_length=10, default='disetujui')
    
    def __str__(self):
        return self.NamaSekolah
    
    def setujukan_pengajuan(self):
        self.status_pengajuan = 'disetujui'
        self.save()
        
    
class PolygonModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    PolygonId = models.BigAutoField(primary_key=True)
    SekolahId = models.ForeignKey(PengajuanSekolahModel, on_delete=models.CASCADE)
    geometri = JSONField()
    warna = models.CharField(max_length=20, null=True, blank=True)

    # def save_geojson(self, geojson_data):
    #     self.geometri = json.dumps(geojson_data)
    #     self.warna = warna_akreditasi(self.SekolahId.AkreditasiSekolah)
    #     geom = GEOSGeometry(json.dumps(geojson_data))
    #     self.save()
        
    def warna_akreditasi(akreditasi):
        if akreditasi == 'A':
            return 'green'
        elif akreditasi == 'B':
            return 'blue'
        elif akreditasi == 'C':
            return 'yellow'
        elif akreditasi == 'TT':
            return 'red'
        else:
            return 'gray'
    
class PengajuanSMAModel(models.Model):
    NILAI_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ) 
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    GuruS1 = models.IntegerField()
    GuruKeseluruhan1 = models.IntegerField()
    GuruBersertifikat = models.IntegerField()
    GuruKeseluruhan2 = models.IntegerField()
    GuruMengajarSesuaiPendidikan = models.IntegerField()
    GuruKeseluruhan3 = models.IntegerField()
    HasilGurus1 = models.IntegerField()
    HasilGuruBersertifikat = models.IntegerField()
    HasilGuruMengajarSesuaiPendidikan = models.IntegerField()
    ipr4 = models.IntegerField(choices=NILAI_CHOICES)
    ipr5 = models.IntegerField(choices=NILAI_CHOICES)
    ipr6 = models.IntegerField(choices=NILAI_CHOICES)
    ipr7 = models.IntegerField(choices=NILAI_CHOICES)
    ipr8 = models.IntegerField(choices=NILAI_CHOICES)
    ipr9 = models.IntegerField(choices=NILAI_CHOICES)
    jumlah_skor = models.FloatField()
    nilai_ipr = models.FloatField()
    
    # komponen mutu lulusan
    butir1 = models.IntegerField(choices=NILAI_CHOICES)
    butir2 = models.IntegerField(choices=NILAI_CHOICES)
    butir3 = models.IntegerField(choices=NILAI_CHOICES)
    butir4 = models.IntegerField(choices=NILAI_CHOICES)
    butir5 = models.IntegerField(choices=NILAI_CHOICES)
    butir6 = models.IntegerField(choices=NILAI_CHOICES)
    butir7 = models.IntegerField(choices=NILAI_CHOICES)
    butir8 = models.IntegerField(choices=NILAI_CHOICES)
    butir9 = models.IntegerField(choices=NILAI_CHOICES)
    butir10 = models.IntegerField(choices=NILAI_CHOICES)
    butir11 = models.IntegerField(choices=NILAI_CHOICES)
    jumlah_mutu_lulusan = models.IntegerField()
    nilai_kompoenen_mutu_lulusan = models.IntegerField()
    nilai_mutu_lulusan = models.IntegerField()
    
    # komponen proses pembelajaran
    butir12 = models.IntegerField(choices=NILAI_CHOICES)
    butir13 = models.IntegerField(choices=NILAI_CHOICES)
    butir14 = models.IntegerField(choices=NILAI_CHOICES)
    butir15 = models.IntegerField(choices=NILAI_CHOICES)
    butir16 = models.IntegerField(choices=NILAI_CHOICES)
    butir17 = models.IntegerField(choices=NILAI_CHOICES)
    butir18 = models.IntegerField(choices=NILAI_CHOICES)
    jumlah_proses_pembelajaran = models.IntegerField()
    nilai_kompoenen_proses_pembelajaran = models.IntegerField()
    nilai_proses_pembelajaran = models.IntegerField()
    
    # komponen mutu guru
    butir19 = models.IntegerField(choices=NILAI_CHOICES)
    butir20 = models.IntegerField(choices=NILAI_CHOICES)
    butir21 = models.IntegerField(choices=NILAI_CHOICES) 
    butir22 = models.IntegerField(choices=NILAI_CHOICES)
    jumlah_mutu_guru = models.IntegerField()
    nilai_kompoenen_mutu_guru = models.IntegerField()
    nilai_mutu_guru = models.IntegerField()
    
    # komponen manajemen sekolah
    butir23 = models.IntegerField(choices=NILAI_CHOICES)
    butir24 = models.IntegerField(choices=NILAI_CHOICES)
    butir25 = models.IntegerField(choices=NILAI_CHOICES)
    butir26 = models.IntegerField(choices=NILAI_CHOICES)
    butir27 = models.IntegerField(choices=NILAI_CHOICES)
    butir28 = models.IntegerField(choices=NILAI_CHOICES)
    butir29 = models.IntegerField(choices=NILAI_CHOICES)
    butir30 = models.IntegerField(choices=NILAI_CHOICES)
    butir31 = models.IntegerField(choices=NILAI_CHOICES)
    butir32 = models.IntegerField(choices=NILAI_CHOICES)
    butir33 = models.IntegerField(choices=NILAI_CHOICES)
    butir34 = models.IntegerField(choices=NILAI_CHOICES)
    butir35 = models.IntegerField(choices=NILAI_CHOICES)
    jumlah_manajemen_sekolah = models.IntegerField()
    nilai_kompoenen_manajemen_sekolah = models.IntegerField()
    nilai_manajemen_sekolah = models.IntegerField()
    
    jumlah_keseluruhan = models.IntegerField()
    
    
class NilaiAkhirModel(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Nilaiid = models.BigAutoField(primary_key=True)
    # NPSN = models.ForeignKey(PengajuanSekolahModel, on_delete=models.CASCADE)
    nilai_akhir = models.FloatField()
    predikat = models.CharField(max_length=1)
    
    
class PengajuanSMKModel(models.Model):
    NILAI_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ) 
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    GuruS1 = models.IntegerField()
    GuruKeseluruhan1 = models.IntegerField()
    GuruBersertifikat = models.IntegerField()
    GuruKeseluruhan2 = models.IntegerField()
    GuruMengajarSesuaiPendidikan = models.IntegerField()
    GuruKeseluruhan3 = models.IntegerField()
    HasilGurus1 = models.IntegerField()
    HasilGuruBersertifikat = models.IntegerField()
    HasilGuruMengajarSesuaiPendidikan = models.IntegerField()
    ipr4 = models.IntegerField(choices=NILAI_CHOICES)
    ipr5 = models.IntegerField(choices=NILAI_CHOICES)
    ipr6 = models.IntegerField(choices=NILAI_CHOICES)
    ipr7 = models.IntegerField(choices=NILAI_CHOICES)
    ipr8 = models.IntegerField(choices=NILAI_CHOICES)
    ipr9 = models.IntegerField(choices=NILAI_CHOICES)
    ipr10 = models.IntegerField(choices=NILAI_CHOICES)
    jumlah_skor = models.FloatField()
    nilai_ipr = models.FloatField()
    
    # komponen mutu lulusan
    butir1 = models.IntegerField(choices=NILAI_CHOICES)
    butir2 = models.IntegerField(choices=NILAI_CHOICES)
    butir3 = models.IntegerField(choices=NILAI_CHOICES)
    butir4 = models.IntegerField(choices=NILAI_CHOICES)
    butir5 = models.IntegerField(choices=NILAI_CHOICES)
    butir6 = models.IntegerField(choices=NILAI_CHOICES)
    butir7 = models.IntegerField(choices=NILAI_CHOICES)
    butir8 = models.IntegerField(choices=NILAI_CHOICES)
    butir9 = models.IntegerField(choices=NILAI_CHOICES)
    butir10 = models.IntegerField(choices=NILAI_CHOICES)
    butir11 = models.IntegerField(choices=NILAI_CHOICES)
    kekhususanbutir36 = models.IntegerField(choices=NILAI_CHOICES)
    kekhususanbutir37 = models.IntegerField(choices=NILAI_CHOICES)
    jumlah_mutu_lulusan = models.IntegerField()
    nilai_kompoenen_mutu_lulusan = models.IntegerField()
    nilai_mutu_lulusan = models.IntegerField()
    
    # komponen proses pembelajaran
    butir12 = models.IntegerField(choices=NILAI_CHOICES)
    butir13 = models.IntegerField(choices=NILAI_CHOICES)
    butir14 = models.IntegerField(choices=NILAI_CHOICES)
    butir15 = models.IntegerField(choices=NILAI_CHOICES)
    butir16 = models.IntegerField(choices=NILAI_CHOICES)
    butir17 = models.IntegerField(choices=NILAI_CHOICES)
    butir18 = models.IntegerField(choices=NILAI_CHOICES)
    kekhususanbutir38 = models.IntegerField(choices=NILAI_CHOICES)
    kekhususanbutir39 = models.IntegerField(choices=NILAI_CHOICES)
    jumlah_proses_pembelajaran = models.IntegerField()
    nilai_kompoenen_proses_pembelajaran = models.IntegerField()
    nilai_proses_pembelajaran = models.IntegerField()
    
    # komponen mutu guru
    butir19 = models.IntegerField(choices=NILAI_CHOICES)
    butir20 = models.IntegerField(choices=NILAI_CHOICES)
    butir21 = models.IntegerField(choices=NILAI_CHOICES) 
    butir22 = models.IntegerField(choices=NILAI_CHOICES)
    kekhususanbutir40 = models.IntegerField(choices=NILAI_CHOICES)
    jumlah_mutu_guru = models.IntegerField()
    nilai_kompoenen_mutu_guru = models.IntegerField()
    nilai_mutu_guru = models.IntegerField()
    
    # komponen manajemen sekolah
    butir23 = models.IntegerField(choices=NILAI_CHOICES)
    butir24 = models.IntegerField(choices=NILAI_CHOICES)
    butir25 = models.IntegerField(choices=NILAI_CHOICES)
    butir26 = models.IntegerField(choices=NILAI_CHOICES)
    butir27 = models.IntegerField(choices=NILAI_CHOICES)
    butir28 = models.IntegerField(choices=NILAI_CHOICES)
    butir29 = models.IntegerField(choices=NILAI_CHOICES)
    butir30 = models.IntegerField(choices=NILAI_CHOICES)
    butir31 = models.IntegerField(choices=NILAI_CHOICES)
    butir32 = models.IntegerField(choices=NILAI_CHOICES)
    butir33 = models.IntegerField(choices=NILAI_CHOICES)
    butir34 = models.IntegerField(choices=NILAI_CHOICES)
    butir35 = models.IntegerField(choices=NILAI_CHOICES)
    kekhususanbutir41 = models.IntegerField(choices=NILAI_CHOICES)
    kekhususanbutir42 = models.IntegerField(choices=NILAI_CHOICES)
    kekhususanbutir43 = models.IntegerField(choices=NILAI_CHOICES)
    kekhususanbutir44 = models.IntegerField(choices=NILAI_CHOICES)
    jumlah_manajemen_sekolah = models.IntegerField()
    nilai_kompoenen_manajemen_sekolah = models.IntegerField()
    nilai_manajemen_sekolah = models.IntegerField()
    
    jumlah_keseluruhan = models.IntegerField()