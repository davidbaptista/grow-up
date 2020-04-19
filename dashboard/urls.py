from django.urls import path

from dashboard import views

urlpatterns = [
	path('dashboard/', views.dashboard, name='dashboard'),
	path('events/', views.events, name='events'),
	path('browse-events/', views.browse_events, name='browse_events'),
	path('browse-events/<region>', views.browse_events, name='browse_events'),
	path('manage-events/', views.manage_events, name='manage_events'),
	path('event/<id>', views.event, name='event'),
	path('about-us/', views.about_us, name='about_us'),
	path('plan-event/', views.plan_event, name='plan_event'),
	path('edit-event/<id>', views.edit_event, name='edit_event'),
	path('attend-event/<id>', views.attend_event, name='attend_event'),
	path('unattend-event/<id>', views.unattend_event, name='unattend_event'),
	path('delete-event/<id>', views.delete_event, name='delete_event'),
	path('profile/', views.profile, name='profile'),
	path('edit-profile/', views.edit_profile, name='edit_profile'),
]
