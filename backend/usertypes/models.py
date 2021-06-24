from datetime import date

from django.conf import settings
from django.db import models


def user_directory_path(instance, filename):
    return 'user/avatar/{0}/{1}'.format(instance.id, filename)


class Patient(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='patient', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=MALE)
    date_of_birth = models.DateField(blank=True, null=True, default=date.today)
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    weight = models.PositiveSmallIntegerField(blank=True, null=True)
    insurance_number = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    
    # to check if this patient can make an appointment.
    is_filled_in = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='doctor', 
                                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    specialty = models.CharField(max_length=255, blank=True, null=True)
    picture = models.ImageField(upload_to=user_directory_path, null=True, 
                                blank=True, default='doctor-default.jpg')
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
