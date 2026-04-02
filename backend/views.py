from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def backend(request, slug=None):
    return HttpResponse("<p>Hello from the backend-side</p>")