# Generated by Django 4.0.4 on 2022-08-20 22:54

from django.db import migrations, models
import pbx.models


class Migration(migrations.Migration):

    dependencies = [
        ("pbx", "0006_sipcontacts"),
    ]

    operations = [
        migrations.AddField(
            model_name="extension",
            name="user",
            field=models.UUIDField(
                blank=True, null=True, validators=[pbx.models.validate_user_exists]
            ),
        ),
    ]
