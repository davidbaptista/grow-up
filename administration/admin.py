from django.contrib import admin
from django.contrib.auth.models import Group

from dashboard.models import OrganisationProfile, VolunteerProfile

admin.site.unregister(Group)


class OrganisationProfileAdmin(admin.ModelAdmin):
	pass

class VolunteerProfileAdmin(admin.ModelAdmin):
	pass


admin.site.register(OrganisationProfile, OrganisationProfileAdmin)
admin.site.register(VolunteerProfile, VolunteerProfileAdmin)
