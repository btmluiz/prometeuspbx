# Generated by Django 4.0.4 on 2022-05-10 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ui", "0004_alter_notification_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="type",
            field=models.SlugField(choices=[("toast", "Toast")], default="toast"),
        ),
    ]
