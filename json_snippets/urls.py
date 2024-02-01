from django.urls import path
from . import views

app_name = "json_snippets"


urlpatterns = [
    path('', views.root_functions_view),
    path('json/', views.django_json_response, name='json_response'),
    path('snippets/', views.snippet_list, name='snippet_list'),
    path('snippets/<int:pk>/', views.snippet_detail, name='snippet_detail'),
]

