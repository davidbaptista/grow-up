import calendar
import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe

from dashboard.forms import EditVolunteerProfileForm, EditOrganisationProfileForm
from dashboard.models import VolunteerProfile, OrganisationProfile
from dashboard.utils import Calendar, previous_date, next_date, get_date


@login_required(redirect_field_name='index')
def dashboard(request):
	date = get_date(request.GET.get('date', None))
	calendar = Calendar()
	cal = calendar.formatmonth(date.year, date.month)
	return render(request, 'dashboard/dashboard.html', {'dashboard': True,
														'calendar': mark_safe(cal),
														'previous_month': previous_date(date),
	                                                    'next_month': next_date(date)})


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


@login_required(redirect_field_name='index')
def edit_profile(request):

	profile = VolunteerProfile.objects.get(user=request.user or None)
	if profile:
		form = EditVolunteerProfileForm(request.POST or None, instance=profile)

	return render(request, 'dashboard/edit_profile.html', {'form': form})