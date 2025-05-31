from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm


# Create your views here.
def homePageView(request):
    return render(request, 'base.html')

def play(request):
    return render(request, 'minesweeper.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        tmp = form.save()
        return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def records(request):
    return render(request, 'records.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        tmp = form.save()
        return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
