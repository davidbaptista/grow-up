from django.shortcuts import render


def index(request):
	return render(request, 'website/index.html')


def organisation(request):
	return render(request, 'website/organisation.html')


def volunteer(request):
	return render(request, 'website/volunteer.html')
