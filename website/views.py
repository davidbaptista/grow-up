from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect

from website.forms import RegisterForm, LoginForm


def index(request):
    return render(request, 'base/index.html')


def login(response):
    if response.method == 'POST':
        form = LoginForm(response.POST)
        if form.is_valid():
            return redirect('index')
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
            email.send()

            if 'volunteer' in response.POST:
                return HttpResponse('Enviamos um email para confirmar o seu registo como voluntário')
            elif 'organization' in response.POST:
                return HttpResponse('Enviamos um email para confirmar o registo como organização.')
    else:
        form = RegisterForm()

    return render(response, 'registration/register.html', {'form': form})


def activate(request):
    pass
