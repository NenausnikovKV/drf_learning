from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "function_view"


urlpatterns = [

    path('', views.redirect_to_root, name="empty_address"),
    path('root/', views.root_functions_view, name="root"),
    path('snippets/', views.snippet_list, name='snippet_list'),
    path('snippets/<int:pk>/', views.snippet_detail, name='snippet_detail'),
    path('snippets/<int:pk>/highlighted', views.snippet_highlighted, name='highlighted'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
