from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path, include
from django.shortcuts import redirect, render

from .views import account_views, author_views, follower_views, node_api, post_views, comment_views, like_views, inbox_views

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
    
    # Account views
    re_path(r"^$", account_views.index, name="index"),
    path('accounts/login/', account_views.signin, name='signin'),
    path('accounts/signup/', account_views.signup, name='signup'),
    path('accounts/logout/', account_views.logout_view, name='logout'),

    # Author views
    path('get_author_id/', author_views.get_author_id, name="get_author_id"),
    path('authors', author_views.AuthorListAPI.as_view(), name='author_list'),
    path('authors/<uuid:author_id>/', author_views.AuthorAPI.as_view(), name='author_api'),

    # Follower views
    path('authors/<uuid:author_id>/followers', follower_views.FollowerListAPI.as_view(), name='followers_list'),
    path('authors/<uuid:author_id>/followers/<uuid:foreign_author_id>/', follower_views.FollowerAPI.as_view(), name="follower_api"),

    # Post views
    path('authors/<uuid:author_id>/posts/<uuid:post_id>/', post_views.SinglePostAPI.as_view(), name="post_single"),
    path('authors/<uuid:author_id>/posts/', post_views.PostAPI.as_view(), name="post"),

    # Comment views
    path('authors/<uuid:author_id>/posts/<uuid:post_id>/comments', comment_views.CommentAPI.as_view(), name="comments"),

   #  # Like views
    path('authors/<uuid:author_id>/posts/<uuid:post_id>/likes', like_views.PostLikeAPI.as_view(), name="post_likes"),
    path('authors/<uuid:author_id>/posts/<uuid:post_id>/comments/<uuid:comment_id>/likes/', like_views.CommentLikeAPI.as_view(), name="comment_likes"),

   # Inbox views
    path('authors/<uuid:author_id>/inbox', inbox_views.InboxAPI.as_view(), name="inbox"),
   #  path('authors/<uuid:author_id>/inbox/', inbox_views.InboxAPI.as_view(), name="inbox1"),

   # Liked Views
    path('authors/<uuid:author_id>/liked/', like_views.PostLikedAPI.as_view(), name="author_liked"),

   # # Liked Views
   #  path('authors/<uuid:author_id>/liked/', inbox_views.InboxLike.as_view(), name="author_liked")

   # Nodes
   path('nodes/tokens/', node_api.get_tokens, name="get_tokens"),
   path('nodes/hostnames/', node_api.get_hostnames, name="get_hostnames"),
   path('nodes/api_endpoints/', node_api.get_api_endpoints, name="get_api_endpoints")

]
