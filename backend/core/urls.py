from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path
from django.shortcuts import redirect, render

from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Peer2Pressure API",
      default_version='v1',
      description="API Docs for Peer2Pressure Social Network",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="admin@peer2pressure.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)



urlpatterns = [
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    re_path(r"^$", views.index, name="index"),
    
    path('get_author_id/', views.CurrentAuthorID.as_view(), name="get_author_id"),

    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout'),
    
    path('authors/', views.AuthorListAPI.as_view(), name='author_list'),
    path('authors/<uuid:author_id>/', views.AuthorAPI.as_view(), name='author_api'),
    path('authors/<uuid:author_id>/followers/', views.FollowerListAPI.as_view(), name='followers_list'),
    path('authors/<uuid:author_id>/followers/<uuid:foreign_author_id>/', views.FollowerAPI.as_view(), name="follower_api"),

    path('authors/<uuid:author_id>/posts/<uuid:post_id>/', views.SinglePostAPI.as_view(), name="post_single"),
    path('authors/<uuid:author_id>/posts/', views.PostAPI.as_view(), name="post"),

    path('authors/<uuid:author_id>/posts/<uuid:post_id>/comments/', views.CommentAPI.as_view(), name="comment"),
    
    path('authors/<uuid:author_id>/posts/<uuid:post_id>/likes/', views.LikeAPI.as_view(), name="like"),
    path('authors/<uuid:author_id>/posts/<uuid:post_id>/comments/<uuid:comment_id>/likes/', views.CommentLikeAPI.as_view(), name="comment_like"),
    path('authors/<uuid:author_id>/inbox/', views.InboxLike.as_view(), name="inbox_like"),

    path('authors/<uuid:author_id>/liked/', views.InboxLike.as_view(), name="author_liked")
      
]