# Generated by Django 4.1.7 on 2023-03-20 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_author_url_alter_comment_url_alter_post_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.URLField(blank=True, default=''),
        ),
    ]
