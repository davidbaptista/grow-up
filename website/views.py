from django.shortcuts import render


def index(request):
	if 'id' in request.session:
		del request.session['id']
	if 'org' in request.session:
		del request.session['org']

	return render(request, 'website/index.html')


def organisation(request):
	return render(request, 'website/organisation.html')


def volunteer(request):
	return render(request, 'website/volunteer.html')
