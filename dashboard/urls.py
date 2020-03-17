from django.urls import path

from dashboard import views

urlpatterns = [
	path('dashboard-reservations/', views.dashboard_reservations, name='dashboard_reservations'),
	path('dashboard-activities/', views.dashboard_activities, name='dashboard_activities'),
	path('dashboard-activities/<region>', views.dashboard_activities, name='dashboard_activities'),
	path('about-us/', views.about_us, name='about_us'),
	path('plan-event/', views.plan_event, name='plan_event'),
	path('edit-event/<event_id>', views.edit_event, name='edit_event'),
	path('attend-event/<event_id>', views.attend_event, name='attend_event'),
	path('delete-event/<event_id>', views.delete_event, name='delete_event'),
	path('profile/', views.profile, name='profile'),
	path('edit-profile/', views.edit_profile, name='edit_profile'),
]
