from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class ApiRootView(APIView):
    # def get(self, request, format=None):
        # return HttpResponse("hello")
    def get(self, request, format=None):
        return Response({
            'users': reverse('snippets:user_list', request=request, format=format),
            'class_snippets': reverse('snippets:snippet_list', request=request, format=format),
            'function_snippets': reverse('function_view:snippet_list', request=request, format=format),
            'json_snippets': reverse("json_snippets:snippet_list", request=request)
        })
