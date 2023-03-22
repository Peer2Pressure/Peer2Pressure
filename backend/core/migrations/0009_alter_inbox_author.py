# Generated by Django 4.1.7 on 2023-03-22 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_author_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inbox',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='inbox', to='core.author'),
        ),
    ]
