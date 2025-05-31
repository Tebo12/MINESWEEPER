from django.urls import path
from .views import homePageView, play, login_view, records,register
urlpatterns = [
    path('', homePageView, name='home'),
    path('play/', play, name='play'),
    path('login/', login_view, name='login'),
    path('records/', records, name='records'),
    path('register/', register, name='register')
]
