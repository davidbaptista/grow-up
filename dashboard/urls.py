from django.urls import path

from dashboard import views

urlpatterns = [
	path('dashboard/', views.dashboard, name='dashboard'),
	path('activities/', views.activities, name='activities'),
	path('reservations/', views.reservations, name='reservations'),
	path('about-us/', views.about_us, name='about_us'),
	path('plan-event/', views.plan_event, name='plan_event'),
	path('profile/', views.profile, name='profile'),
	path('edit-profile/', views.edit_profile, name='edit_profile'),
]
