from django.contrib.auth.models import User, AbstractUser
from django.db import models
from multiselectfield import MultiSelectField


class AgeRange(models.Model):
	name = models.CharField(max_length=16)

	def __str__(self):
		return self.name


class OrganisationType(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name


class Profile:
	pass


class VolunteerProfile(models.Model, Profile):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	middle_names = models.CharField(max_length=255, blank=True)
	gender = models.BooleanField(default=False, blank=True)
	age = models.SmallIntegerField(blank=True, null=True, default=0)
	image = models.FileField(upload_to='static/media/users/', blank=True)
	occupation = models.CharField(max_length=127, blank=True)
	location = models.CharField(max_length=255, blank=True)
	phone_number = models.IntegerField(blank=True, null=True, default=0)


class OrganisationProfile(models.Model, Profile):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	organisation_name = models.CharField(max_length=255, blank=True)
	representative_name = models.CharField(max_length=255, blank=True)
	is_active = models.BooleanField(default=False)
	age_range = models.ManyToManyField(AgeRange, blank=True)
	organisation_type = models.ManyToManyField(OrganisationType, blank=True)
