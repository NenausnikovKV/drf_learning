from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.ApiRootView.as_view()),
    path("class/", include('snippets.urls')),
    path("functions/", include("function_view.urls")),
    path("json/", include("json_snippets.urls")),

    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
]
