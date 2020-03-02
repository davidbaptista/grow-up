from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from dashboard.forms import EditVolunteerProfileForm, EditOrganisationProfileForm, PlanEventForm
from dashboard.models import VolunteerProfile, OrganisationProfile
from dashboard.utils import Calendar, previous_date, next_date, get_date


@login_required
def dashboard(request):
	date = get_date(request.GET.get('date', None))
	calendar = Calendar(locale='pt_PT.utf8')
	cal = calendar.formatmonth(date.year, date.month)

	region = request.GET.get('region', None)
	if region:
		print('hi')

	if 'profile_type' not in request.session:
		try:
			organisation = OrganisationProfile.objects.get(user=request.user)
			request.session['profile_type'] = 'organisation'
			request.session['profile_id'] = organisation.pk
		except OrganisationProfile.DoesNotExist:
			try:
				volunteer = VolunteerProfile.objects.get(user=request.user)
				request.session['profile_type'] = 'volunteer'
				request.session['profile_id'] = volunteer.pk
			except VolunteerProfile.DoesNotExist:
				redirect('error')
			except KeyError:
				redirect('error')

	return render(request, 'dashboard/dashboard.html', {'calendar': mark_safe(cal),
	                                                    'previous_month': previous_date(date),
	                                                    'next_month': next_date(date)})


@login_required
def activities(request):
	return render(request, 'dashboard/activities.html')


@login_required
def reservations(request):
	return render(request, 'dashboard/reservations.html')


@login_required
def about_us(request):
	return render(request, 'dashboard/about_us.html')


@login_required
def profile(request):
	if request.session['profile_type'] == 'volunteer':
		prof = VolunteerProfile.objects.get(pk=request.session['profile_id'])
	else:
		prof = OrganisationProfile.objects.get(pk=request.session['profile_id'])

	return render(request, 'dashboard/profile.html', {'profile': prof})


@login_required
def edit_profile(request):
	if request.session['profile_type'] == 'volunteer':
		profile = VolunteerProfile.objects.get(pk=request.session['profile_id'])
		form = EditVolunteerProfileForm(request.POST or None, request.FILES or None, instance=profile)
	else:
		profile = OrganisationProfile.objects.get(pk=request.session['profile_id'])
		form = EditOrganisationProfileForm(request.POST or None, request.FILES or None, instance=profile)

	if request.method == 'POST' and form.is_valid():
		form.save()

		return redirect('profile')

	return render(request, 'dashboard/edit_profile.html', {'form': form})


@login_required
def plan_event(request):
	if request.session['profile_type'] == 'organisation':
		form = PlanEventForm(request.POST or None, request.FILES or None)

		if request.method == 'POST' and form.is_valid():
			event = form.save(commit=False)

			event.organisation = OrganisationProfile.objects.get(pk=request.session['profile_id'])

			return redirect('dashboard')

		return render(request, 'dashboard/plan_event.html', {'form': form})
