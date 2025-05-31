from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def homePageView(request):
    return render(request, 'base.html')

def play(request):
    return render(request, 'minesweeper.html')

def login_view(request):
    return render(request, 'login.html')

def records(request):
    return render(request, 'records.html')

def register(request):
    return render(request, 'register.html')