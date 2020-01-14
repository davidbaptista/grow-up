from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class OrganizationType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Profile:
    pass


class VolunteerProfile(models.Model, Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=127)
    middle_names = models.CharField(max_length=255)
    last_name = models.CharField(max_length=127)
    gender = models.BooleanField()
    age = models.SmallIntegerField()
    image = models.FileField(upload_to='static/media/users/')
    occupation = models.CharField(max_length=127)
    location = models.CharField(max_length=255)
    phone_number = models.IntegerField()


class OrganizationProfile(models.Model, Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255)
    representative_name = models.CharField(max_length=255)

    class AgeGroup(models.TextChoices):
        CHILDREN = 'CR', _('Crianças')
        TEENS = 'JV', _('Jovens')
        ADULTS = 'AD', _('Adultos')
        ELDERLY = 'ID', _('Idosos')

    age_group = models.CharField(
        max_length=2,
        choices=AgeGroup.choices,
        default=AgeGroup.ADULTS
    )

    organization_types = models.ManyToManyField(OrganizationType)
