from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect

from website.forms import RegisterForm, LoginForm


def index(request):
    return render(request, 'base/index.html')


@login_required(redirect_field_name='index')
def dashboard(request):
    return render(request, 'base/dashboard.html')


def login_request(response):
    if response.method == 'POST':
        form = LoginForm(response.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(response, user)
                return redirect('dashboard')
    else:
        form = LoginForm()

    return render(response, 'registration/login.html', {'form': form})


def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            email_subject = 'Ative a sua conta'

            message = 'ola'

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            #email.send()

            if 'volunteer' in response.POST:
                return HttpResponse('Enviamos um email para confirmar o seu registo como voluntário')
            elif 'organization' in response.POST:
                return HttpResponse('Enviamos um email para confirmar o registo como organização.')
    else:
        form = RegisterForm()

    return render(response, 'registration/register.html', {'form': form})


def activate(request):
    pass
