from django.urls import path
from .views import homePageView, play, logout_view, records, RegisterView, stats, LoginView
urlpatterns = [
    path('', homePageView, name='home'),
    path('play/', play, name='play'),
    path('login/', LoginView.as_view(), name='login'),
    path('records/', records, name='records'),
    path('register/', RegisterView.as_view(), name='register'),
    path('stats/', stats, name='stats'),
    path('logout/', logout_view, name='logout')
]
