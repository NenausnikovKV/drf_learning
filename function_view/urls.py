from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, view_functions, view_simple_function

app_name = "function_view"


urlpatterns = [
    path('', views.root_functions_view),

    path('snippets/', view_functions.drf_style_snippet_list, name='snippet_list'),
    path('snippets/<int:pk>/', view_functions.drf_style_snippet_detail, name='snippet_detail'),
    path('snippets/<int:pk>/highlighted', view_functions.snippet_highlighted, name='simple_highlighted'),
]

urlpatterns = format_suffix_patterns(urlpatterns)