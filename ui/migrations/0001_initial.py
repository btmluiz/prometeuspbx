# Generated by Django 4.0.4 on 2022-05-08 22:36

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("created_at", models.DateTimeField(auto_created=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=40, null=True)),
                ("content", models.TextField()),
                (
                    "type",
                    models.SlugField(
                        choices=[
                            ("toast", "Toast"),
                            ("alert_success", "Alert Success"),
                            ("alert_fail", "Alert Fail"),
                            ("alert_warning", "Alert Warning"),
                        ],
                        default="toast",
                    ),
                ),
                ("is_read", models.BooleanField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
