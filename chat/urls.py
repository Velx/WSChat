from django.urls import path

from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
]