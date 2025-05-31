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
from random import randint


# Create your views here.
def homePageView(request):
    return render(request, 'base.html')


def play(request):
    a = 10
    b = 10
    field = [[0] * a for i in range(b)]

    bombs = 5

    for i in range(bombs):
        while True:
            x = randint(0, a - 1)
            y = randint(0, b - 1)
            if field[x][y] == 0:
                field[x][y] = -1  # клетка с бомбой
                break

    for i in range(a):
        for j in range(b):
            if field[i][j] == -1:
                place_numbers(field, a, b, i, j)
    """
        for l in field:
        print(l)
    """
    player_view = [[''] * a for i in range(b)]
    return render(request, 'minesweeper.html', {'player_view': player_view})


def place_numbers(field, a, b, i, j):
    for x1 in range(i - 1, i + 2):
        for y1 in range(j - 1, j + 2):
            if (0 <= x1 < a) and (0 <= y1 < b):
                if field[x1][y1] != -1:
                    field[x1][y1] += 1


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
            message = 'Не удалось войти'
            return render(request, self.template_name, context={'form': form, 'message': message})
        return render(request, self.template_name, context={'form': form, 'message': 'Неверная форма'})


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
