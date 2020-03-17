from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from dashboard.forms import EditVolunteerProfileForm, EditOrganisationProfileForm, PlanEventForm
from dashboard.models import VolunteerProfile, OrganisationProfile, Event, Region
from dashboard.utils import Calendar, previous_date, next_date, get_date


@login_required
def dashboard_reservations(request):
	date = get_date(request.GET.get('date', None))
	calendar = Calendar(locale='pt_PT.utf8')
	cal = calendar.formatmonth(date.year, date.month)
	events = None

	if 'profile_type' not in request.session:
		if OrganisationProfile.objects.filter(user=request.user).count() > 0:
			organisation = OrganisationProfile.objects.get(user=request.user)
			request.session['profile_type'] = 'organisation'
			request.session['profile_id'] = organisation.pk
			events = Event.objects.filter(organisation=organisation, end__gte=datetime.now())
		elif VolunteerProfile.objects.filter(user=request.user).count() > 0:
			volunteer = VolunteerProfile.objects.get(user=request.user)
			request.session['profile_type'] = 'volunteer'
			request.session['profile_id'] = volunteer.pk
			events = volunteer.events.filter(end__gte=datetime.now())
		else:
			redirect('error')

	else:
		if request.session['profile_type'] == 'volunteer':
			volunteer = VolunteerProfile.objects.get(user=request.user)
			events = volunteer.events.filter(end__gte=datetime.now())
		else:
			organisation = OrganisationProfile.objects.get(user=request.user)
			events = Event.objects.filter(organisation=organisation, end__gte=datetime.now())

	return render(request, 'dashboard/dashboard_reservations.html', {'calendar': mark_safe(cal),
	                                                                 'previous_month': previous_date(date),
	                                                                 'next_month': next_date(date),
	                                                                 'events': events})


@login_required
def dashboard_activities(request, region=None):
	region_name = None
	if request.session['profile_type'] == 'volunteer':
		if region:
			region_name = Region.objects.get(description=region)
			events = Event.objects.filter(location__description=region, start__gt=datetime.now())
		else:
			events = Event.objects.filter(start__gt=datetime.now())

		profile = VolunteerProfile.objects.get(pk=request.session['profile_id'])

		return render(request, 'dashboard/dashboard_activities.html', {'events': events,
		                                                               'region': region_name,
		                                                               'profile': profile,
		                                                               'is_organisation': False})
	elif request.session['profile_type'] == 'organisation':
		if region:
			region_name = Region.objects.get(description=region)

			events = Event.objects.filter(organisation_id=request.session['profile_id'],
			                              location__description=region,
			                              start__gt=datetime.now())
		else:
			events = Event.objects.filter(organisation_id=request.session['profile_id'], start__gt=datetime.now())

		return render(request, 'dashboard/dashboard_activities.html', {'events': events,
		                                                               'region': region_name,
		                                                               'is_organisation': True})
	else:
		return redirect('error')


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

			event.save()

			return redirect('dashboard_activities')

		return render(request, 'dashboard/plan_event.html', {'form': form})


@login_required
def edit_event(request, event_id):
	try:
		event = Event.objects.get(pk=event_id)
	except Event.DoesNotExist:
		return redirect('index')

	if request.session['profile_type'] == 'organisation' and event.organisation.id == request.session['profile_id']:
		form = PlanEventForm(request.POST or None, instance=event)

		if request.method == 'POST' and form.is_valid():
			form.save()

			return redirect(dashboard_activities)

		return render(request, 'dashboard/edit_event.html', {'form': form})

	return redirect('index')


@login_required
def attend_event(request, event_id):
	try:
		event = Event.objects.get(pk=event_id)
	except Event.DoesNotExist:
		return redirect('index')

	if request.session['profile_type'] == 'volunteer':
		try:
			volunteer = VolunteerProfile.objects.get(pk=request.session['profile_id'])
		except VolunteerProfile.DoesNotExist:
			return redirect('index')

		if volunteer.events.filter(pk=event_id).count() == 0:
			volunteer.events.add(event)
			return redirect('dashboard_reservations')
		else:
			return redirect('error')


@login_required
def delete_event(request, event_id):
	try:
		event = Event.objects.get(pk=event_id)
	except Event.DoesNotExist:
		return redirect('index')

	if request.session['profile_type'] == 'organisation' and event.organisation.id == request.session['profile_id']:
		Event.objects.get(pk=event_id).delete()
		return redirect('dashboard_activities')

	return redirect('index')
