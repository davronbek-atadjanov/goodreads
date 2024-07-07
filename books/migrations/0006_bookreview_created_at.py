# Generated by Django 5.0.6 on 2024-07-04 17:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0005_book_created_time_book_updated_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookreview",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]