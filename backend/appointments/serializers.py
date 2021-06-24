from rest_framework import serializers
from usertypes.serializers import DoctorSerializer, PatientSerializer

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
         
    class Meta:
        model = Appointment
        fields = (
            'id',
            'doctor',
            'patient',
            'is_available',
            'date',
            'timeslot',
            'symptom',
        )         
