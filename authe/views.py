from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import UserForm
# Create your views here.


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')

    return render(request, 'auth/login.html', {})


def logout_view(request):
    logout(request)
    return redirect('/')


def signup_view(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'], data['email'], data['password'])
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()
        return redirect('/')

    return render(request, 'auth/signup.html', {'form': form})
