from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from dashboard.models import VolunteerProfile, OrganisationProfile


@login_required(redirect_field_name='index')
def dashboard(request):
	return render(request, 'dashboard/dashboard.html', {'dashboard': True})


@login_required(redirect_field_name='index')
def activities(request):
	return render(request, 'dashboard/activities.html', {'dashboard': True})


@login_required(redirect_field_name='index')
def reservations(request):
	return render(request, 'dashboard/reservations.html', {'dashboard': True})


@login_required(redirect_field_name='index')
def about_us(request):
	return render(request, 'dashboard/about_us.html', {'dashboard': True})


@login_required(redirect_field_name='index')
def profile(request):
	try:
		prof = VolunteerProfile.objects.get(user=request.user)
		volunteer = True
	except ObjectDoesNotExist:
		prof = OrganisationProfile.objects.get(user = request.user)
		volunteer = False

	return render(request, 'dashboard/profile.html', {'profile': prof, 'dashboard': True, 'volunteer': volunteer})
