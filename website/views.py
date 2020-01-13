from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.utils.translation import gettext_lazy as _

from website.forms import RegisterForm


def index(request):
    return render(request, 'base/index.html')


def login(request):
    return render(request, 'registration/login.html')


def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('index')
    else:
        form = RegisterForm()

    return render(response, 'registration/register.html', {'form': form})
