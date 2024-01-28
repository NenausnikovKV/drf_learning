from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from snippets.models import SimpleSnippet
from snippets.serializers import SimpleSnippetSerializer


@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = SimpleSnippet.objects.all()
        serializer = SimpleSnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SimpleSnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = SimpleSnippet.objects.get(pk=pk)
    except SimpleSnippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SimpleSnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SimpleSnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'POST'])
def drf_style_snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    Can use format suffix, e.g. ".json"
    """
    if request.method == 'GET':
        snippets = SimpleSnippet.objects.all()
        serializer = SimpleSnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = request.user
        serializer = SimpleSnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def drf_style_snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = SimpleSnippet.objects.get(pk=pk)
    except SimpleSnippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SimpleSnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SimpleSnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def snippet_highlighted(request, pk):
    """
        Retrieve snippet highlighted.
        Return HttpResponse.
    """
    try:
        snippet = SimpleSnippet.objects.get(pk=pk)
    except SimpleSnippet.DoesNotExist:
        return HttpResponse(status=404)
    else:
        return HttpResponse(snippet.highlighted)
