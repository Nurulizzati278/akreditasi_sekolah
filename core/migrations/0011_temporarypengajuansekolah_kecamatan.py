# Generated by Django 5.0.6 on 2024-06-05 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_pengajuansekolahmodel_kecamatan'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporarypengajuansekolah',
            name='Kecamatan',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]
