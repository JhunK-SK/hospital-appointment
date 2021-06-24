from django.contrib import admin

from .models import Doctor, Patient

admin.site.register(Patient)
admin.site.register(Doctor)
