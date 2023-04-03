# Generated by Django 4.1.7 on 2023-04-03 12:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('m_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('id', models.URLField()),
                ('host', models.URLField(default='http://localhost:8000')),
                ('username', models.CharField(blank=True, max_length=512)),
                ('name', models.CharField(blank=True, max_length=512)),
                ('url', models.URLField()),
                ('email', models.CharField(blank=True, max_length=512)),
                ('password', models.CharField(blank=True, max_length=512)),
                ('avatar', models.URLField(blank=True, default='', null=True)),
                ('github', models.URLField(blank=True, default='', null=True)),
                ('user', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('m_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('type', models.CharField(default='comment', max_length=512)),
                ('id', models.URLField(default='')),
                ('comment', models.TextField(default='')),
                ('url', models.URLField(default='')),
                ('content_type', models.CharField(default='text/plain', max_length=512)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('object', models.URLField(default='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('m_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('api_endpoint', models.CharField(default='', max_length=512)),
                ('token', models.CharField(default='', max_length=512)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('m_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('id', models.URLField(default='')),
                ('url', models.URLField(default='')),
                ('title', models.CharField(blank=True, default='', max_length=512)),
                ('content', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('visibility', models.CharField(default='PUBLIC', max_length=512)),
                ('source', models.URLField(blank=True)),
                ('origin', models.URLField(blank=True)),
                ('description', models.CharField(blank=True, default='', max_length=512)),
                ('content_type', models.CharField(max_length=512)),
                ('comments', models.URLField(default='')),
                ('unlisted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='core.author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('m_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('type', models.CharField(default='like', max_length=512)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('summary', models.CharField(default='', max_length=512)),
                ('object', models.URLField(default='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_like', to='core.post')),
            ],
        ),
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('m_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('type', models.CharField(default='post', max_length=512)),
                ('object_id', models.UUIDField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='inbox', to='core.author')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('m_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('summary', models.CharField(default='', max_length=512)),
                ('approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('from_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='core.author')),
                ('to_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='core.author')),
            ],
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('m_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('type', models.CharField(default='like', max_length=512)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('summary', models.CharField(default='', max_length=512)),
                ('object', models.URLField(default='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.author')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_like', to='core.comment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='core.post'),
        ),
        migrations.AddConstraint(
            model_name='postlike',
            constraint=models.UniqueConstraint(fields=('author', 'post'), name='A user can only like post onces'),
        ),
        migrations.AddConstraint(
            model_name='follower',
            constraint=models.UniqueConstraint(fields=('from_author', 'to_author'), name='There can only be this relation between two authors'),
        ),
        migrations.AddConstraint(
            model_name='author',
            constraint=models.UniqueConstraint(fields=('id',), name='Unique user properties'),
        ),
    ]
