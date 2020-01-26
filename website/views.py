from django.contrib.auth import authenticate, login as logon, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from website.forms import RegisterFormVolunteer, LoginForm, RegisterFormOrganisation, PasswordChangeForm, \
    PasswordResetForm

'''Intro page views'''
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'intro/index.html')


def organisation(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'intro/organisation.html')


def volunteer(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'intro/volunteer.html')


'''Dashboard views '''
@login_required(redirect_field_name='index')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

'''Authentication views'''
def login(response):
    if response.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(data=response.POST or None)
    if response.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            logon(response, user)
            return redirect('dashboard')
    else:
        return render(response, 'authentication/login.html', {'form': form})


def register_organisation(response):
    if response.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterFormOrganisation(data=response.POST or None)
    if response.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.save()

        return HttpResponse('Enviamos um email para confirmar o seu registo como organização')

    return render(response, 'authentication/register.html', {'form': form,
                                                             'type': 'organisation',
                                                             'message': 'organização'})


def register_volunteer(response):
    if response.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterFormVolunteer(data=response.POST or None)
    if response.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.save()

        '''email_subject = 'Ative a sua conta de voluntário'
        message = 'Change later'
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send() '''

        return HttpResponse('Enviamos um email para confirmar o seu registo como voluntário')

    return render(response, 'authentication/register.html', {'form': form,
                                                             'type': 'volunteer',
                                                             'message': 'voluntário'})

@login_required(redirect_field_name='index')
def change_password(response):
    form = PasswordChangeForm(data=response.POST or None, user=response.user)

    if response.method == 'POST' and form.is_valid():
        form.save()
        update_session_auth_hash(response, form.user)
        return redirect('dashboard')

    return render(response, 'authentication/change_password.html', {'form': form})

