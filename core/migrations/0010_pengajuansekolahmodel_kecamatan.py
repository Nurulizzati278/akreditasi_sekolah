# Generated by Django 5.0.6 on 2024-06-05 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_pengajuansekolahmodel_jumlahguru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pengajuansekolahmodel',
            name='Kecamatan',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]