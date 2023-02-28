from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path
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
    
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('authors/', views.AuthorListAPI.as_view(), name='author_list'),
    path('authors/<uuid:author_id>', views.AuthorAPI.as_view(), name='author_api'),
    path('authors/<uuid:author_id>/followers', views.FollowerListAPI.as_view(), name='followers_list'),
    path('authors/<uuid:author_id>/followers/<uuid:foreign_author_id>', views.FollowerAPI.as_view(), name="follower_api"),
      
]