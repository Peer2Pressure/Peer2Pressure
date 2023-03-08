# Generated by Django 4.1.7 on 2023-03-08 04:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('host', models.URLField(default='http://127.0.0.1:8000')),
                ('username', models.CharField(blank=True, max_length=300)),
                ('first_name', models.CharField(blank=True, max_length=300)),
                ('last_name', models.CharField(blank=True, max_length=300)),
                ('url', models.CharField(blank=True, max_length=300)),
                ('email', models.CharField(blank=True, max_length=300)),
                ('password', models.CharField(blank=True, max_length=300)),
                ('avatar', models.URLField(blank=True, default=None, null=True)),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='author_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('from_author_request', models.BooleanField(default=False)),
                ('to_author_request', models.BooleanField(default=False)),
                ('from_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='core.author')),
                ('to_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='core.author')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('url', models.CharField(blank=True, max_length=300)),
                ('title', models.CharField(blank=True, default='', max_length=300)),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_images')),
                ('content', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_private', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='core.author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='core.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('comment', models.TextField(default='')),
                ('url', models.CharField(blank=True, max_length=300)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='relation',
            constraint=models.UniqueConstraint(fields=('from_author', 'to_author'), name='There can only be this relation between two authors'),
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('author', 'post'), name='A user can only like post onces'),
        ),
        migrations.AddConstraint(
            model_name='author',
            constraint=models.UniqueConstraint(fields=('username', 'email', 'password'), name='Unique user properties'),
        ),
    ]