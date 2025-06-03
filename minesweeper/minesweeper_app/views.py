import datetime

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
from .models import Results
from django.contrib.auth import get_user_model


# Create your views here.
def homePageView(request):
    return render(request, 'index.html')


def play(request):
    a = 20
    b = 20
    bombs = 5

    titles_to_win = a * b - bombs

    opened_titles = request.session.get('opened_titles', 0)
    field = request.session.get('field', field_generation(a, b, bombs))
    player_view = request.session.get('player_view', player_view_generation(a, b))
    boom = False
    win = False

    title_open = 0
    flag_set = 0

    if restart := request.GET.get('restart'):
        field = field_generation(a, b, bombs)
        player_view = player_view_generation(a, b)
        opened_titles = 0

    else:
        if x := request.GET.get('x'):
            if y := request.GET.get('y'):
                if rightClick := request.GET.get('rightClick'):
                    if player_view[int(x)][int(y)] == 'X':
                        player_view[int(x)][int(y)] = ''
                    else:
                        if player_view[int(x)][int(y)] == '':
                            player_view[int(x)][int(y)] = 'X'
                            flag_set = 1

                else:
                    if player_view[int(x)][int(y)] == '':
                        opened_titles += 1
                        player_view[int(x)][int(y)] = field[int(x)][int(y)]
                        title_open = 1
                    if field[int(x)][int(y)] == -1:
                        boom = True
                        title_open = 1
                        field = field_generation(a, b, bombs)
                        player_view = player_view_generation(a, b)
        else:
            field = field_generation(a, b, bombs)
            player_view = player_view_generation(a, b)
            opened_titles = 0

    request.session['field'] = field
    request.session['player_view'] = player_view
    request.session['opened_titles'] = opened_titles

    if opened_titles >= titles_to_win and not boom:
        win = True
    if request.user.is_authenticated:
        user_model = get_user_model()
        user = user_model.objects.get(id=request.user.id)
        if boom or win:
            if time := int(request.GET.get('time')):
                record = Results(user=user, won=win, time=time)
                record.save()
        user.number_of_titles += title_open
        user.number_of_flags += flag_set
        user.save(update_fields=["number_of_titles", "number_of_flags"])

    return render(request, 'minesweeper.html', {'player_view': player_view,
                                                'boom': boom, 'win': win, 'bombs_count': bombs})


def player_view_generation(a, b):
    return [[''] * a for i in range(b)]


def field_generation(a, b, bombs):
    field = [[0] * a for i in range(b)]

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

    return field


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
    best = []
    user_model = get_user_model()
    user_list = list(user_model.objects.all())

    for user in user_list:
        wins = 0
        time = float(0)
        results = list(Results.objects.filter(user=user))
        for obj in results:
            if obj.won:
                wins += 1
            time += round((obj.time / 3600), 1)

        best.append({'login': user.username, 'wins': wins, 'time': time})

    best.sort(key=lambda i: i['wins'], reverse=True)
    best = best[:10]
    print(best)
    return render(request, 'records.html', {'best': best})


@login_required
def stats(request):
    user_model = get_user_model()
    user = user_model.objects.get(id=request.user.id)
    cells_opened = user.number_of_titles
    flags_placed = user.number_of_flags

    wins = 0
    losses = 0
    hours_played = 0

    results = list(Results.objects.filter(user=user))
    for obj in results:
        if obj.won:
            wins += 1
        else:
            losses += 1
        hours_played += obj.time / 3600

    if wins+losses != 0:
        win_rate = wins/(wins+losses) * 100
    else:
        win_rate = 0
    return render(request, 'stats.html', {'wins': wins, 'losses': losses,
                                          'cells_opened': cells_opened, 'flags_placed': flags_placed,
                                          'hours_played': hours_played, 'win_rate': win_rate
                                          })


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
