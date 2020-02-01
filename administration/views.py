from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from dashboard.models import OrganisationProfile


@login_required(redirect_field_name='index')
def staff(request):
	if request.user.is_staff:
		return render(request, 'staff/staff.html')
	else:
		return redirect('index')


@login_required(redirect_field_name='index')
def manage_organisations(request):
	if request.user.is_staff:
		organisations = OrganisationProfile.objects.filter(is_active=True, user__is_active=False)
		return render(request, 'staff/manage_organisations.html', {'organisations': organisations})
	else:
		return redirect('index')


@login_required(redirect_field_name='index')
def accept_organisation(request, organisation_id):
	if request.user.is_staff:
		user = OrganisationProfile.objects.filter(id=organisation_id).first().user
		user.is_active = True
		user.save()

		return redirect('manage_organisations')
	else:
		return redirect('index')


@login_required(redirect_field_name='index')
def decline_organisation(request, organisation_id):
	if request.user.is_staff:
		profile = OrganisationProfile.objects.filter(id=organisation_id).first()
		profile.user.delete()
		profile.delete()

		return redirect('manage_organisations')
	else:
		return redirect('index')
