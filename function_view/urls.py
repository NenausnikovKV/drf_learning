from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, view_functions, view_simple_function

urlpatterns = [
    path('', views.root_functions_view),

    path('json/', view_simple_function.django_json_response, name='json_response'),
    path('json_snippets/', view_simple_function.snippet_list, name='django_style_snippet_list'),
    path('json_snippets/<int:pk>/', view_simple_function.snippet_detail, name='django_style_snippet_detail'),

    path('simple_snippets/', view_functions.drf_style_snippet_list, name='simple_snippet_list'),
    path('simple_snippets/<int:pk>/', view_functions.drf_style_snippet_detail, name='simple_snippet_detail'),
    path('simple_snippets/<int:pk>/highlighted', view_functions.snippet_highlighted, name='simple_highlighted'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
