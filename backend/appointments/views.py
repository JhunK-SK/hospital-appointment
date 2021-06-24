from collections import OrderedDict

from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from usertypes.models import Doctor, Patient

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentPagination(PageNumberPagination):
    page_size = 12
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total_page', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class AppointmentViewSet(viewsets.ModelViewSet):
    
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = AppointmentPagination
    
    # return queryset upon request user's usertype(manager, doctor, patient).
    def get_queryset(self):
        user_type = self.request.user.user_type
        
        if user_type == 'manager':
            queryset = Appointment.objects.all()
            keyword = self.request.query_params.get('q', None)
            date = self.request.query_params.get('date', None)
            
            # return a filtered queryset when keyword, date parameters exist.
            if keyword or date:
                obj = queryset.filter(
                    Q(doctor__first_name__icontains=keyword) |
                    Q(doctor__last_name__icontains=keyword) |
                    Q(patient__first_name__icontains=keyword) |
                    Q(patient__last_name__icontains=keyword)
                )
                if date:
                    return obj.filter(Q(date__exact=date))
                else:
                    return obj
            else:
                return queryset
        
        elif user_type == 'patient':
            patient = Patient.objects.get(user=self.request.user)
            queryset = Appointment.objects.filter(patient=patient)
        
        elif user_type == 'doctor':
            doctor = Doctor.objects.get(user=self.request.user)
            queryset = Appointment.objects.filter(doctor=doctor)
        
        return queryset
    
    # since django receives ids of doctor and patient from the front,
    # objects of doctor and patient should be defined to pass them to serializers.
    def perform_create(self, serializer):
        doctor_id = self.request.data.get('doctor')
        patient_id = self.request.data.get('patient')
        doctor = Doctor.objects.get(pk=doctor_id)
        patient = Patient.objects.get(pk=patient_id)
        serializer.save(doctor=doctor, patient=patient)
        
        
# returns timeslots of an appointment of a selected doctor on a requested date
# to display which timeslots are not available.
class AppointmentListAPIView(ListAPIView):
    
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        doctor_id = self.request.query_params.get('doctor', None)
        date = self.request.query_params.get('date', None)

        if doctor_id and date:
            return self.queryset.filter(doctor=doctor_id, date=date)
        
        return self.queryset
