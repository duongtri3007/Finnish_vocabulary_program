from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.from django.shortcuts import render

def frontend(request, slug=None):
    return render(request, 'frontend/template_web.html')