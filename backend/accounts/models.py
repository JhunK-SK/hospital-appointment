from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email')
        
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    DOCTOR = 'doctor'
    MANAGER = 'manager'
    PATIENT = 'patient'
    
    USER_TYPE = (
        (DOCTOR, 'Doctor'),
        (MANAGER, 'Manager'),
        (PATIENT, 'Patient'),
    )
    
    # basic information
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    # for admin page
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # three types that users can be
    user_type = models.CharField(max_length=20, choices=USER_TYPE, 
                                 default=PATIENT)
    
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']
    
    class Meta:
        ordering = ['-date_joined']
    
    
    def __str__(self):
        return self.email
    
    @property
    def get_full_name(self):
        return f'{self.first_name.lower().title()} {self.last_name.lower().title()}'
    
    def get_joined_data_formatted(self):
        return self.date_joined.strftime('%d.%m.%Y')
