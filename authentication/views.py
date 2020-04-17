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
from formtools.wizard.views import SessionWizardView

from authentication.forms import LoginForm, PasswordChangeForm, RegisterForm, RegisterOrganisationForm, \
	RegisterOrganisationProfileForm, RegisterVolunteerForm
from dashboard.models import VolunteerProfile, OrganisationProfile
from dashboard.aux import *

authentication_token = PasswordResetTokenGenerator()


def login(request):
	if request.user.is_authenticated:
		return redirect('index')

	# Session variables used everywhere
	if 'profile_type' in request.session:
		del request.session['profile_type']
	if 'profile_id' in request.session:
		del request.session['profile_id']

	# Session variables used in authentication methods
	if 'id' in request.session:
		del request.session['id']
	if 'org' in request.session:
		del request.session['org']

	form = LoginForm(data=request.POST or None)

	if request.method == 'POST' and form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)

		if user is not None:
			logon(request, user)

			if is_volunteer(request) or is_organisation(request):
				return redirect('dashboard')
			else:
				return redirect('error')
	else:
		return render(request, 'authentication/login.html', {'form': form})


class RegisterOrganisationWizard(SessionWizardView):
	template_name = 'authentication/register.html'
	form_list = [RegisterForm, RegisterOrganisationForm]

	def get_context_data(self, form, **kwargs):
		context = super().get_context_data(form=form, **kwargs)
		context.update({'type': 'organisation', 'msg': 'organização'})

		if self.steps.current == '0':
			context.update(
				{'message': 'Insira um email associado à organização, e escolha um nome de utilizador e password'})
		elif self.steps.current == '1':
			context.update({'message': 'Preencha as seguintes informações relativas à organização'})

		return context

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('index')
		else:
			return super(RegisterOrganisationWizard, self).dispatch(request, *args, **kwargs)

	def done(self, form_list, **kwargs):
		l = list(form_list)
		user = l[0].save(commit=False)
		profile = l[1].save(commit=False)

		user.is_active = False
		profile.user = user

		user.save()
		profile.save()

		self.request.session['id'] = profile.pk
		return redirect('register_organisation_profile')


def register_organisation_profile(response):
	if response.user.is_authenticated:
		return redirect('index')

	form = RegisterOrganisationProfileForm(data=response.POST or None)

	if response.method == 'POST' and form.is_valid():
		org_id = response.session['id']
		profile = OrganisationProfile.objects.get(pk=org_id)

		profile.age_range.set(form.cleaned_data['age_range'])
		profile.organisation_type.set(form.cleaned_data['organisation_type'])
		profile.save()

		send_email(response, profile.user.pk, True)
		response.session['id'] = profile.user.pk
		response.session['org'] = True

		return redirect('register_done')
	else:
		return render(response, 'authentication/register_organisation_profile.html', {'form': form})


class RegisterVolunteerWizard(SessionWizardView):
	template_name = 'authentication/register.html'
	form_list = [RegisterForm, RegisterVolunteerForm]

	def get_context_data(self, form, **kwargs):
		context = super().get_context_data(form=form, **kwargs)
		context.update({'type': 'volunteer', 'msg': 'voluntário'})

		if self.steps.current == 0:
			context.update(
				{'message': 'Preencha com um email para associar à conta e escolha um nome de utilizador e password'})
		elif self.steps.current == 1:
			context.update(
				{'message': 'Preencha com os seus dados pessoais'})

		return context

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('index')
		else:
			return super(RegisterVolunteerWizard, self).dispatch(request, *args, **kwargs)

	def done(self, form_list, **kwargs):
		l = list(form_list)
		user = l[0].save(commit=False)
		profile = l[1].save(commit=False)

		profile.user = user
		user.is_active = False

		user.save()
		profile.save()

		send_email(self.request, user.pk, False)

		self.request.session['id'] = profile.user.pk
		self.request.session['org'] = False
		return redirect('register_done')


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
			org = True
		else:
			user.is_active = True
			user.save()
			org = False

		return render(response, 'authentication/register_complete.html', {'org': org})
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


def resend_email(request):
	if request.user.is_authenticated:
		return redirect('index')

	send_email(request, request.session['id'], request.session['org'])

	return redirect('register_done')


def send_email(request, user_id, is_organisation):
	if is_organisation:
		email_subject = 'Ative a sua conta de organização'
		template = 'authentication/register_email_organisation.html'
	else:
		email_subject = 'Ativa a sua conta de voluntário'
		template = 'authentication/register_email_volunteer.html'

	user = User.objects.get(pk=user_id)

	message = render_to_string(template, {
		'user': user,
		'domain': get_current_site(request),
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': authentication_token.make_token(user)
	})

	to_email = user.email
	email = EmailMessage(email_subject, message, to=[to_email])
	email.send()
