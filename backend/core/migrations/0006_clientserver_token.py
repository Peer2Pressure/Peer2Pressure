# Generated by Django 4.1.7 on 2023-03-26 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_clientserver_delete_serveradmin'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientserver',
            name='token',
            field=models.CharField(default='', max_length=512),
        ),
    ]
