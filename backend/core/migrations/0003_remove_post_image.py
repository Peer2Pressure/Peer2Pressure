# Generated by Django 4.1.7 on 2023-03-30 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_post_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]