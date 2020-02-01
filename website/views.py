from django.shortcuts import render


def index(request):
	return render(request, 'intro/index.html')


def organisation(request):
	return render(request, 'intro/organisation.html')


def volunteer(request):
	return render(request, 'intro/volunteer.html')
