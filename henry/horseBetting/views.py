from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    output = 'test- index'
    return HttpResponse(output)

def add(request):
    output = 'test- add'
    return HttpResponse(output)

