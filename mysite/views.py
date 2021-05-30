from django.shortcuts import render
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

def check(request):
    return render(request, 'temp.html')