from django.contrib.auth import authenticate, login as logon, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from website.forms import RegisterFormVolunteer, LoginForm, RegisterFormOrganisation, PasswordChangeForm
from website.models import VolunteerProfile, OrganisationProfile

authentication_token = PasswordResetTokenGenerator()


def index(request):
    return render(request, 'intro/index.html')


def organisation(request):
    return render(request, 'intro/organisation.html')


def volunteer(request):
    return render(request, 'intro/volunteer.html')


@login_required(redirect_field_name='index')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def login(response):
    if response.user.is_authenticated:
        return redirect('index')
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
        return redirect('index')
    form = RegisterFormOrganisation(data=response.POST or None)

    if response.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        profile = OrganisationProfile()
        profile.user = user
        user.save()
        profile.save()

        email_subject = 'Ative a sua conta de organização'
        message = render_to_string('authentication/register_email.html', {
            'user': user,
            'domain': get_current_site(response),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': authentication_token.make_token(user)
        })

        to_email = form.cleaned_data.get('email')
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()
        return redirect('register_done')

    return render(response, 'authentication/register.html', {'form': form,
                                                             'type': 'organisation',
                                                             'message': 'organização'})


def register_volunteer(response):
    if response.user.is_authenticated:
        return redirect('index')

    form = RegisterFormVolunteer(data=response.POST or None)

    if response.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        profile = VolunteerProfile()
        profile.user = user
        user.save()
        profile.save()

        email_subject = 'Ative a sua conta de voluntário'
        message = render_to_string('authentication/register_email.html', {
            'user': user,
            'domain': get_current_site(response),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': authentication_token.make_token(user)
        })

        to_email = form.cleaned_data.get('email')
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()

        return redirect('register_done')

    return render(response, 'authentication/register.html', {'form': form,
                                                             'type': 'volunteer',
                                                             'message': 'voluntário'})


def register_done(response):
    if response.user.is_authenticated:
        return redirect('index')

    return render(response, 'authentication/register_done.html')


def register_complete(response, uidb64, token):
    if response.user.is_authenticated:
        return redirect('index')

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and authentication_token.check_token(user, token):
        profile = OrganisationProfile.objects.filter(user=user).first()

        if profile:
            profile.is_active = True
            profile.save()
        else:
            user.is_active = True
            user.save()
            logon(response, user)

        return redirect('dashboard')
    else:
        return HttpResponse('Link inválido')


@login_required(redirect_field_name='index')
def password_change(response):
    form = PasswordChangeForm(data=response.POST or None, user=response.user)

    if response.method == 'POST' and form.is_valid():
        form.save()
        update_session_auth_hash(response, form.user)
        return redirect('dashboard')

    return render(response, 'authentication/password_change.html', {'form': form})


@login_required(redirect_field_name='index')
def staff(request):
    if request.user.is_staff:
        return render(request, 'staff/staff.html')
    else:
        return redirect('index')


@login_required(redirect_field_name='index')
def manage_organisations(request):
    if request.user.is_staff:
		#organisations = OrganisationProfile.objects.filter(is_active=True, )
        return render(request, 'staff/manage_organisations.html')
    else:
        return redirect('index')
