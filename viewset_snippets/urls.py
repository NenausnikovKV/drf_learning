from django.urls import path, include
from rest_framework.routers import DefaultRouter

from viewset_snippets import views

# Create a router and register our ViewSets with it.
view_set_router = DefaultRouter()
view_set_router.register(r'viewsnippets', views.SnippetViewSet, basename='snippet')
view_set_router.register(r'users', views.UserViewSet, basename='user')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(view_set_router.urls)),
]