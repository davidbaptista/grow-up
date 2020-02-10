from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from dashboard.forms import EditVolunteerProfileForm
from dashboard.models import VolunteerProfile, OrganisationProfile
from dashboard.utils import Calendar, previous_date, next_date, get_date


@login_required(redirect_field_name='index')
def dashboard(request):
	date = get_date(request.GET.get('date', None))
	calendar = Calendar()
	cal = calendar.formatmonth(date.year, date.month)
	return render(request, 'dashboard/dashboard.html', {'calendar': mark_safe(cal),
														'previous_month': previous_date(date),
	                                                    'next_month': next_date(date)})


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
		volunteer = True
	except ObjectDoesNotExist:
		prof = OrganisationProfile.objects.get(user = request.user)
		volunteer = False

	return render(request, 'dashboard/profile.html', {'profile': prof, 'is_volunteer': volunteer})


@login_required(redirect_field_name='index')
def edit_profile(request):
	prof = VolunteerProfile.objects.get(user=request.user or None)
	if prof:
		form = EditVolunteerProfileForm(request.POST or None, request.FILES or None, instance=prof)

		if request.method == 'POST' and form.is_valid():
			form.save()

			return redirect('profile')
	else:
		return HttpResponse('404')

	return render(request, 'dashboard/edit_profile.html', {'form': form})
