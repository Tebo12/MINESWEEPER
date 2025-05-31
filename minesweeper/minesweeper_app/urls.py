from django.urls import path
from .views import homePageView, play, login_view, records

urlpatterns = [
    path('', homePageView, name='home'),
    path('play/', play, name='play'),
    path('login/', login_view, name='login'),
    path('records/', records, name='records'),
]
