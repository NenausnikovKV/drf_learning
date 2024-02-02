from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "function_view"


urlpatterns = [
    path('', views.root_functions_view),

    path('snippets/', views.snippet_list, name='snippet_list'),
    path('snippets/<int:pk>/', views.snippet_detail, name='snippet_detail'),
    path('snippets/<int:pk>/highlighted', views.snippet_highlighted, name='simple_highlighted'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
