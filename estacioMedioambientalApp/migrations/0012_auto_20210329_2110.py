# Generated by Django 3.1.7 on 2021-03-29 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estacioMedioambientalApp', '0011_client_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='token',
            field=models.TextField(verbose_name='Token'),
        ),
        migrations.CreateModel(
            name='RegistreMovil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora', models.DateTimeField(verbose_name='Hora de dades')),
                ('valor', models.TextField(verbose_name='Valor')),
                ('latitudReal', models.FloatField(verbose_name='latitud')),
                ('longitudReal', models.FloatField(verbose_name='longitud')),
                ('localitzacio', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='estacioMedioambientalApp.location', verbose_name='Sensor')),
                ('sensor', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='estacioMedioambientalApp.sensor', verbose_name='Sensor')),
            ],
        ),
    ]