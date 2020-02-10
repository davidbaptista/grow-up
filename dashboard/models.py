from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from grow_up import settings


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
	last_name = models.CharField(max_length=255, blank=True)
	first_name = models.CharField(max_length=255, blank=True)
	middle_names = models.CharField(max_length=255, blank=True, null=True)
	gender = models.BooleanField(default=False, blank=True)
	birth_date = models.DateField(blank=True, null=True)
	occupation = models.CharField(max_length=127, blank=True, null=True)
	location = models.CharField(max_length=255, blank=True, null=True)
	phone_number = models.CharField(blank=True, null=True, default=0, max_length=12)
	image = models.ImageField(upload_to='volunteers/', blank=True, null=True,
	                         validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])


class OrganisationProfile(models.Model, Profile):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	organisation_name = models.CharField(max_length=255, blank=True)
	representative_name = models.CharField(max_length=255, blank=True)
	is_active = models.BooleanField(default=False)
	age_range = models.ManyToManyField(AgeRange, blank=True)
	organisation_type = models.ManyToManyField(OrganisationType, blank=True)
	image = models.ImageField(upload_to='organisations/', blank=True,
	                          validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])


class Event(models.Model):
	day = models.DateField(blank=True, null=True)
	start_time = models.TimeField(blank=True, null=True)
	end_time = models.TimeField(blank=True, null=True)
	title = models.CharField(max_length=255, blank=False, null=False)
	description = models.TextField(blank=True, null=True)
	organisation = models.OneToOneField(OrganisationProfile, on_delete=models.CASCADE)

	def clean(self):
		if self.end_time <= self.start_time:
			raise ValidationError('O fim do evento deve ser após o seu inicio')
