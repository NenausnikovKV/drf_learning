from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views, view_functions

urlpatterns = [
    path('', views.ApiRootView.as_view()),

    path('simple_snippets/', view_functions.drf_style_snippet_list, name='simple_snippet-list'),
    path('simple_snippets/<int:pk>/', view_functions.drf_style_snippet_detail, name='simple_snippet-detail'),
    path('simple_snippets/<int:pk>/highlighted', view_functions.snippet_highlighted, name='simple_snippet-detail'),

    path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),

    path('users/', views.UserList.as_view(), name="user-list"),
    path('users/<int:pk>/', views.UserDetail.as_view(), name="user-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
