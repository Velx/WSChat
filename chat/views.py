from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        print(1)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print(2)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            print('logined')
            return redirect('chat')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
