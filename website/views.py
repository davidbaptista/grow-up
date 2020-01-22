from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from website.forms import RegisterForm
from website.token import account_activation_token


def index(request):
    return render(request, 'base/index.html')


def login(request):
    return render(request, 'registration/login.html')


def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(response)

            email_subject = 'Activate Your Account'
            message = render_to_string('registration/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
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
