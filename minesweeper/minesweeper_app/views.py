from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


# Create your views here.
def homePageView(request):
    return render(request, 'base.html')

def play(request):
    return render(request, 'minesweeper.html')

class LoginView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to your home page
            message = 'Login failed!'
            return render(request, self.template_name, context={'form': form, 'message': message})
        return render(request, self.template_name, context={'form': form, 'message': 'Invalid form'})

class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    template_name = 'register.html'

def records(request):
    return render(request, 'records.html')

@login_required
def stats(request):
    return render(request, 'stats.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

