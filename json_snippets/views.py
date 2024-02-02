from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse as drf_reverse

from .models import CodeSnippet
from .serializers import CodeSnippetSerializer


def root_functions_view(request):
    addresses = {
        "json_response": drf_reverse("json_snippets:json_response", request=request),
        "snippet_list": drf_reverse("json_snippets:snippet_list", request=request),
    }
    return JsonResponse(data=addresses)


def django_json_response(request):
    response_data = {"greeting": "hi"}
    return JsonResponse(data=response_data)


@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = CodeSnippet.objects.all()
        serializer = CodeSnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CodeSnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = CodeSnippet.objects.get(pk=pk)
    except CodeSnippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CodeSnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CodeSnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

# todo add snippet_highlighted with html tempolate