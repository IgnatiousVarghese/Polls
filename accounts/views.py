from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import Registerform, Loginform
from django.contrib import messages


def register(request):
    form = Registerform()
    if request.method == 'POST':
        form = Registerform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            c_password = form.cleaned_data['c_password']
            if User.objects.filter(username= username).exists():
                form.add_error('username' ,  "username already taken")
            elif c_password == password:
                user = User(username=username)
                user.set_password(password)
                user.save()
                return redirect('accounts:login')

            else:
                form.add_error(field='c_password', error="password mismatch!!")
        else:
            form.add_error(None, "username already taken")
    content = {
        'form': form
    }
    return render(request, 'accounts/register.html', content)


def login(request):
    form = Loginform()
    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(request=request, username=username, password=password)
            if user is not None:
                auth.login(request=request, user=user)
                return render(request, 'home.html')
            else:
                form.add_error('password', "incorrect username or password")
    
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth.logout(request)
    return render(request, 'home.html')
