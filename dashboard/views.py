from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from dashboard.forms import EditVolunteerProfileForm, EditOrganisationProfileForm
from dashboard.models import VolunteerProfile, OrganisationProfile
from dashboard.utils import Calendar, previous_date, next_date, get_date


@login_required(redirect_field_name='index')
def dashboard(request):
	date = get_date(request.GET.get('date', None))
	calendar = Calendar(locale='pt_PT.utf8')
	cal = calendar.formatmonth(date.year, date.month)
	try:
		OrganisationProfile.objects.get(user=request.user)
		is_organisation = True
	except ObjectDoesNotExist:
		is_organisation = False
	return render(request, 'dashboard/dashboard.html', {'calendar': mark_safe(cal),
	                                                    'previous_month': previous_date(date),
	                                                    'next_month': next_date(date),
	                                                    'is_organisation': is_organisation},)


@login_required(redirect_field_name='index')
def activities(request):
	return render(request, 'dashboard/activities.html')


@login_required(redirect_field_name='index')
def reservations(request):
	return render(request, 'dashboard/reservations.html')


@login_required(redirect_field_name='index')
def about_us(request):
	return render(request, 'dashboard/about_us.html')


@login_required(redirect_field_name='index')
def profile(request):
	try:
		prof = VolunteerProfile.objects.get(user=request.user)
		is_volunteer = True
	except ObjectDoesNotExist:
		prof = OrganisationProfile.objects.get(user=request.user)
		is_volunteer = False

	return render(request, 'dashboard/profile.html', {'profile': prof, 'is_volunteer': is_volunteer})


@login_required(redirect_field_name='index')
def edit_profile(request):
	try:
		vol = VolunteerProfile.objects.get(user=request.user or None)
		form = EditVolunteerProfileForm(request.POST or None, request.FILES or None, instance=vol)
	except VolunteerProfile.DoesNotExist:
		try:
			org = OrganisationProfile.objects.get(user=request.user or None)
			form = EditOrganisationProfileForm(request.POST or None, request.FILES or None, instance=org)
		except OrganisationProfile.DoesNotExist:
			return HttpResponse('Error')

	if request.method == 'POST' and form.is_valid():
		form.save()

		return redirect('profile')

	return render(request, 'dashboard/edit_profile.html', {'form': form})


@login_required
def plan_event(request):
	return render(request, 'dashboard/plan_event.html')
