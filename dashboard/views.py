from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from dashboard.aux import get_organisation, get_volunteer, is_volunteer, is_organisation
from dashboard.forms import EditVolunteerProfileForm, EditOrganisationProfileForm, PlanEventForm
from dashboard.models import VolunteerProfile, OrganisationProfile, Event, Region
from dashboard.utils import Calendar, previous_date, next_date, get_date


@login_required
def dashboard_reservations(request):
	events = None
	date = get_date(request.GET.get('date', None))
	day = request.GET.get('day', None)

	if 'profile_type' not in request.session:
		if OrganisationProfile.objects.filter(user=request.user).count() > 0:
			organisation = OrganisationProfile.objects.get(user=request.user)
			request.session['profile_type'] = 'organisation'
			request.session['profile_id'] = organisation.pk
			events = Event.objects.filter(organisation=organisation, start__month=date.month, end__gte=datetime.now())
		elif VolunteerProfile.objects.filter(user=request.user).count() > 0:
			volunteer = VolunteerProfile.objects.get(user=request.user)
			request.session['profile_type'] = 'volunteer'
			request.session['profile_id'] = volunteer.pk
			events = volunteer.events.filter(start__month=date.month, end__gte=datetime.now())
		else:
			redirect('error')
	else:
		if request.session['profile_type'] == 'volunteer':
			volunteer = VolunteerProfile.objects.get(user=request.user)
			events = volunteer.events.filter(start__month=date.month, end__gte=datetime.now())
		else:
			organisation = OrganisationProfile.objects.get(user=request.user)
			events = Event.objects.filter(start__month=date.month, organisation=organisation, end__gte=datetime.now())

	calendar = Calendar(locale='pt_PT.utf8')
	cal = calendar.formatmonth(date.year, date.month, events, True)

	if day and events:
		return render(request, 'dashboard/dashboard_reservations.html', {'calendar': mark_safe(cal),
		                                                                 'previous_month': previous_date(date),
		                                                                 'next_month': next_date(date),
		                                                                 'events': events.filter(start__day=day)})
	else:
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
	if is_volunteer(request):
		profile = get_volunteer(request)
		form = EditVolunteerProfileForm(request.POST or None, request.FILES or None, instance=profile)
	elif is_organisation(request):
		profile = get_organisation(request)
		form = EditOrganisationProfileForm(request.POST or None, request.FILES or None, instance=profile)
	else:
		return redirect('error')

	if request.method == 'POST' and form.is_valid():
		form.save()

		return redirect('profile')

	return render(request, 'dashboard/edit_profile.html', {'form': form})


@login_required
def plan_event(request):
	if is_organisation(request):
		form = PlanEventForm(request.POST or None, request.FILES or None)

		if request.method == 'POST' and form.is_valid():
			event = form.save(commit=False)

			event.organisation = get_organisation(request)

			event.save()

			return redirect('dashboard_activities')

		return render(request, 'dashboard/plan_event.html', {'form': form})


@login_required
def edit_event(request, event_id):
	try:
		event = Event.objects.get(pk=event_id)
	except Event.DoesNotExist:
		return redirect('index')

	if is_organisation(request) and event.organisation.id == request.session['profile_id']:
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
		return redirect('error')

	if is_volunteer(request):
		volunteer = get_volunteer(request)

		if not volunteer:
			return redirect('error')

		if volunteer.events.filter(pk=event_id).count() == 0:
			volunteer.events.add(event)
			return redirect('dashboard_reservations')
		else:
			return redirect('error')


@login_required
def unattend_event(request, event_id):
	try:
		event = Event.objects.get(pk=event_id)
	except Event.DoesNotExist:
		return redirect('error')

	if is_volunteer(request):
		volunteer = get_volunteer(request)
		if volunteer.events.filter(id=event.id).count() == 1 and event.end.replace(
				tzinfo=None) >= datetime.now().replace(tzinfo=None):
			volunteer.events.remove(event)
			return redirect('dashboard_reservations')
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
