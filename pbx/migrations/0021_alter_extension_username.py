# Generated by Django 4.1 on 2022-08-30 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pbx", "0020_sipaor_sipauth_sipendpoint"),
    ]

    operations = [
        migrations.AlterField(
            model_name="extension",
            name="username",
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
