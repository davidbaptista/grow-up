from django.shortcuts import render


def index(request):
	if not request.user.is_authenticated and 'profile_id' in request.session:
		del request.session['profile_id']
	if not request.user.is_authenticated and 'profile_type' in request.session:
		del request.session['profile_type']

	return render(request, 'website/index.html')


def organisation(request):
	return render(request, 'website/organisation.html')


def volunteer(request):
	return render(request, 'website/volunteer.html')
