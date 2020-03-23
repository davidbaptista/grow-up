from dashboard.models import VolunteerProfile, OrganisationProfile


def is_volunteer(request):
	if 'profile_type' and 'profile_id' in request.session:
		return request.session['profile_type'] == 'volunteer'
	else:
		return False


def is_organisation(request):
	if 'profile_type' and 'profile_id' in request.session:
		return request.session['profile_type'] == 'organisation'
	else:
		return False


def get_volunteer(request):
	if is_volunteer(request):
		try:
			profile = VolunteerProfile.objects.get(pk=request.session['profile_id'])
			return profile
		except VolunteerProfile.DoesNotExist:
			return None
	return None


def get_organisation(request):
	if is_organisation(request):
		try:
			profile = OrganisationProfile.objects.get(pk=request.session['profile_id'])
			return profile
		except OrganisationProfile.DoesNotExist:
			return None
	return None
