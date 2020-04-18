from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from dashboard.aux import get_organisation, get_volunteer, is_volunteer, is_organisation
from dashboard.forms import EditVolunteerProfileForm, EditOrganisationProfileForm, PlanEventForm
from dashboard.models import VolunteerProfile, OrganisationProfile, Event, Region
from dashboard.utils import Calendar, previous_date, next_date, get_date


@login_required
def dashboard(request):
	events = None
	date = get_date(request.GET.get('date', None))
	day = request.GET.get('day', None)

	if is_organisation(request):
		organisation = get_organisation(request)

		if organisation:
			events = Event.objects.filter(organisation=organisation, start__month=date.month)
		else:
			return redirect('error')

	elif is_volunteer(request):
		volunteer = get_volunteer(request)

		if volunteer:
			events = volunteer.events.filter(start__month=date.month, end__gte=datetime.now())
		else:
			return redirect('error')

	else: 
		return redirect('error')
	
	if day and events:
		events = events.filter(start__day=day)

	calendar = Calendar(locale='pt_PT.utf8').formatmonth(date.year, date.month, events, True)

	return render(request, 'dashboard/dashboard.html',	{'calendar': mark_safe(calendar),
														'previous_month': previous_date(date),
														'next_month': next_date(date),
														'events': events})


@login_required
def events(request):
	if is_organisation(request):
		return redirect(manage_events)
	elif is_volunteer(request):
		return redirect(browse_events)
	
	
@login_required
def manage_events(request):
	return render(request, 'dashboard/manage_events.html')

@login_required
def browse_events(request, region=None):
	region_name = None
	profile = get_volunteer(request)

	if profile:
		if region:
			region_name = Region.objects.get(description=region)
			# Events which have not started in this region
			events = Event.objects.filter(location__description=region, start__gt=datetime.now()) 
		else:
			# Events which have not started
			events = Event.objects.filter(start__gt=datetime.now())

		return render(request, 'dashboard/browse_events.html',	{'events': events,
																'region': region_name,
																'profile': profile,
																'is_organisation': False})
	else:
		return redirect('error')


@login_required
def profile(request):
	if is_volunteer(request):
		profile = get_volunteer(request)
		profile_type = 'volunteer'
	elif is_organisation(request):
		profile = get_organisation(request)
		profile_type = 'organisation'

	else:
		return redirect('error')

	return render(request, 'dashboard/profile.html', {'profile': profile, 'profile_type': profile_type})


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

			return redirect('activities')

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

			return redirect(activities)

		return render(request, 'dashboard/edit_event.html', {'form': form})

	return redirect('index')


@login_required
def attend_event(request, event_id):
	if Event.objects.filter(pk=event_id).count() == 1:
		event = Event.objects.get(pk=event_id)
	else:
		return redirect('error')

	if is_volunteer(request):
		volunteer = get_volunteer(request)

		if not volunteer:
			return redirect('error')

		if volunteer.events.filter(pk=event_id).count() == 0:
			volunteer.events.add(event)
			return redirect('dashboard')
		else:
			return redirect('error')


@login_required
def unattend_event(request, event_id):
	if Event.objects.filter(pk=event_id).count() == 1:
		event = Event.objects.get(pk=event_id)
	else:
		return redirect('error')

	if is_volunteer(request):
		volunteer = get_volunteer(request)
		if volunteer.events.filter(id=event.id).count() == 1 and event.end.replace(
				tzinfo=None) >= datetime.now().replace(tzinfo=None):
			volunteer.events.remove(event)
			return redirect('dashboard')
	return redirect('error')


@login_required
def delete_event(request, event_id):
	if Event.objects.filter(pk=event_id).count() == 1:
		event = Event.objects.get(pk=event_id)
	else:
		return redirect('error')

	if is_organisation(request) and event.organisation.id == request.session['profile_id']:
		Event.objects.get(pk=event_id).delete()
		return redirect('browse_events')

	return redirect('index')

@login_required
def about_us(request):
	return render(request, 'dashboard/about_us.html')
