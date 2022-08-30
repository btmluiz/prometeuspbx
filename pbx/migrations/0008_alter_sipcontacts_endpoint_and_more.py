# Generated by Django 4.0.4 on 2022-08-21 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pbx", "0007_extension_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sipcontacts",
            name="endpoint",
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="sipcontacts",
            name="outbound_proxy",
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="sipcontacts",
            name="via_addr",
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]