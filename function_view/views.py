from django.http import HttpResponse
from django.shortcuts import render



def root_functions_view(request):
    return HttpResponse("hello")
