from django.shortcuts import render
from dashboard.aux import *


def index(request):
	if is_volunteer(request):
		return render(request, 'website/index.html', {'user_type': 'volunteer'})
	elif is_organisation(request):
		return render(request, 'website/index.html', {'user_type': 'organisation'})
	else:
		return render(request, 'website/index.html')


def organisation(request):
	return render(request, 'website/organisation.html')


def volunteer(request):
	return render(request, 'website/volunteer.html')
