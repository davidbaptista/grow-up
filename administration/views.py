from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from dashboard.models import OrganisationProfile


@login_required(redirect_field_name='index')
def administration(request):
	if request.user.is_staff:
		return render(request, 'administration/administration.html',  {'is_administration': True})
	else:
		return redirect('index')


@login_required(redirect_field_name='index')
def manage_organisations(request):
	if request.user.is_staff:
		organisations = OrganisationProfile.objects.filter(is_active=True, user__is_active=False)
		return render(request, 'administration/manage_organisations.html', {'organisations': organisations,
		                                                                    'is_administration': True})
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
