from django.contrib import admin
from .models import Author, Post, Comment, Relation, PostLike, CommentLike, Inbox
# Register your models here.

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Relation)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(Inbox)
