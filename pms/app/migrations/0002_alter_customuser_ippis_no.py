# Generated by Django 5.0.1 on 2024-01-25 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='ippis_no',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
