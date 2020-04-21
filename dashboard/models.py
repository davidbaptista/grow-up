import os

from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.dispatch import receiver


class AgeRange(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class OrganisationType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Profile:
    pass


class OrganisationProfile(models.Model, Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation_name = models.CharField(max_length=255, blank=True)
    representative_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)
    age_range = models.ManyToManyField(AgeRange, blank=True)
    organisation_type = models.ManyToManyField(OrganisationType, blank=True)
    image = models.ImageField(upload_to='organisations/', blank=True, null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])


@receiver(models.signals.post_delete, sender=OrganisationProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=OrganisationProfile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        organisation = OrganisationProfile.objects.get(pk=instance.pk)
        if organisation.image:
            old_file = organisation.image
        else:
            return False
    except OrganisationProfile.DoesNotExist:
        return False

    new_file = instance.image
    if old_file.url and not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class Event(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey(Region, on_delete=models.CASCADE)
    address = models.CharField(max_length=512, blank=True, null=True)
    organisation = models.ForeignKey(OrganisationProfile, on_delete=models.CASCADE)
    age_range = models.ManyToManyField(AgeRange, blank=True)
    organisation_type = models.ManyToManyField(OrganisationType, blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])

    def clean(self):
        if self.end and self.start:
            if self.end <= self.start:
                raise ValidationError('O fim do evento deve ser após o seu inicio')


class VolunteerProfile(models.Model, Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=512, blank=True, null=True)
    gender = models.BooleanField(default=False, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    occupation = models.CharField(max_length=127, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, max_length=12)
    image = models.ImageField(upload_to='volunteers/', blank=True, null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])
    events = models.ManyToManyField(Event, blank=True)


@receiver(models.signals.post_delete, sender=VolunteerProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=VolunteerProfile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        volunteer = VolunteerProfile.objects.get(pk=instance.pk)
        if volunteer.image:
            old_file = volunteer.image
        else:
            return False
    except VolunteerProfile.DoesNotExist:
        return False

    new_file = instance.image
    if old_file.url and not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
