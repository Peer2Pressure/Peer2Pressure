# Generated by Django 4.1.7 on 2023-03-23 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="host",
            field=models.URLField(default="http://localhost:8000"),
        ),
    ]