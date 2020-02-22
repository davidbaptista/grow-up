from django.shortcuts import render


def error(request):
	return render(request, 'generic/error.html')