# Generated by Django 4.1.7 on 2023-03-30 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentlike',
            name='post',
        ),
        migrations.AddField(
            model_name='commentlike',
            name='object',
            field=models.URLField(default=''),
        ),
        migrations.AddField(
            model_name='commentlike',
            name='summary',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='commentlike',
            name='type',
            field=models.CharField(default='like', max_length=300),
        ),
    ]
