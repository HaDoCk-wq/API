# Generated by Django 3.1.7 on 2021-03-26 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estacioMedioambientalApp', '0005_auto_20210326_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensortype',
            name='tipus',
            field=models.CharField(max_length=50, verbose_name='Tipus de sensor'),
        ),
    ]
