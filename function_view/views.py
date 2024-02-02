from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CodeSnippet
from .serializers import CodeSerializer


def root_functions_view(request):
    return HttpResponse("hello")


@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    Can use format suffix, e.g. ".json"
    """
    if request.method == 'GET':
        snippets = CodeSnippet.objects.all()
        serializer = CodeSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = CodeSnippet.objects.get(pk=pk)
    except CodeSnippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CodeSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CodeSerializer(snippet, data=request.data)
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
        snippet = CodeSnippet.objects.get(pk=pk)
    except CodeSnippet.DoesNotExist:
        return HttpResponse(status=404)
    else:
        return HttpResponse(snippet.highlighted)
