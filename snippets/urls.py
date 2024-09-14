from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "snippets"

urlpatterns = [
    path('', views.ApiRootView.as_view(), name="root"),

    path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),

    path('users/', views.UserList.as_view(), name="user-list"),
    path('users/<int:pk>/', views.UserDetail.as_view(), name="user-detail"),
]


urlpatterns = format_suffix_patterns(urlpatterns)
