from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def root_functions_view(request):


    return HttpResponse("hello")
