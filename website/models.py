from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


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

    class AgeGroup(models.TextChoices):
        CHILDREN = 'CR', _('Crianças')
        TEENS = 'JV', _('Jovens')
        ADULTS = 'AD', _('Adultos')
        ELDERLY = 'ID', _('Idosos')

    age_group = models.CharField(
        max_length=2,
        choices=AgeGroup.choices,
        blank=True
    )

    organisation_types = models.ManyToManyField(OrganisationType, blank=True)
