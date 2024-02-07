import json

from django import shortcuts
from django.http import HttpResponse, HttpResponsePermanentRedirect
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.renderers import BrowsableAPIRenderer, OpenAPIRenderer, JSONRenderer, StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse as drf_reverse

from .models import CodeSnippet
from .permissions import IsOwnerOrReadOnly
from .serializers import CodeSerializer


def redirect_to_root(request):
    address = shortcuts.reverse("function_view:root")
    return HttpResponsePermanentRedirect(address)


@api_view(['GET'])
# @renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def root_functions_view(request, format=None):
    addresses = {
        "snippet_list": drf_reverse("function_view:snippet_list", request=request),
    }
    return Response(addresses)


@api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
@permission_classes([IsAuthenticatedOrReadOnly])
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
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
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
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def snippet_highlighted(request, pk):
    try:
        snippet = CodeSnippet.objects.get(pk=pk)
    except CodeSnippet.DoesNotExist:
        return HttpResponse(status=404)
    else:
        return HttpResponse(snippet.highlighted)
