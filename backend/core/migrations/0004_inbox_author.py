# Generated by Django 4.1.7 on 2023-03-21 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_follower_remove_inbox_author_remove_inbox_post_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inbox',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.author'),
        ),
    ]
