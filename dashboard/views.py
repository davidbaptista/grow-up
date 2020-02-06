from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(redirect_field_name='index')
def dashboard(request):
	return render(request, 'dashboard/dashboard.html')


@login_required(redirect_field_name='index')
def profile(request):
	return render(request, 'dashboard/profile.html')