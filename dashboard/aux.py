from dashboard.models import VolunteerProfile, OrganisationProfile


def is_volunteer(request):
	return request.user.is_authenticated and VolunteerProfile.objects.filter(user=request.user).count() == 1


def is_organisation(request):
	return request.user.is_authenticated and OrganisationProfile.objects.filter(user=request.user).count() == 1


def get_volunteer(request):
	if is_volunteer(request):
		try:
			return VolunteerProfile.objects.get(user=request.user)
		except VolunteerProfile.DoesNotExist:
			return None
	return None


def get_organisation(request):
	if is_organisation(request):
		try:
			return OrganisationProfile.objects.get(user=request.user)
		except OrganisationProfile.DoesNotExist:
			return None
	return None
