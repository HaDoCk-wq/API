# Generated by Django 3.1.7 on 2021-03-26 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estacioMedioambientalApp', '0007_auto_20210326_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='altitud',
            field=models.FloatField(null=True, verbose_name='altitud'),
        ),
    ]