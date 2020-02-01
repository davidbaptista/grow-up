from django.urls import path

from administration import views

urlpatterns = [
	path('staff/', views.staff, name='staff'),
	path('manage-organisations/', views.manage_organisations, name='manage_organisations'),
	path('accept-organisation/<organisation_id>', views.accept_organisation, name='accept_organisation'),
	path('decline-organisation/<organisation_id>', views.decline_organisation, name='decline_organisation'),
]
