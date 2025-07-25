# Generated by Django 5.1.6 on 2025-07-19 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomerAddress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("address_line", models.CharField(max_length=100)),
                ("telephone", models.CharField(max_length=100)),
                ("zip_code", models.CharField(max_length=20)),
                ("city", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
            ],
        ),
    ]
