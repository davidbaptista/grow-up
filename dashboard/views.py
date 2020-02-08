import calendar
import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.utils.safestring import mark_safe

from dashboard.models import VolunteerProfile, OrganisationProfile
from dashboard.utils import Calendar, previous_month, next_month, get_date


@login_required(redirect_field_name='index')
def dashboard(request):
	today = get_date(request.GET.get('month', None))
	calendar = Calendar()
	cal = calendar.formatmonth(today.year, today.month)
	return render(request, 'dashboard/dashboard.html', {'dashboard': True,
														'calendar': mark_safe(cal),
														'previous_month': previous_month(today),
	                                                    'next_month': next_month(today)})


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
