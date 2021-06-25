from accounts.models import CustomUser
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser

from .models import Doctor, Patient
from .serializers import (DoctorPictureSerializer, DoctorSerializer,
                          PatientSerializer)


class PatientViewSet(viewsets.ModelViewSet):
    
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        search_type = self.request.query_params.get('searchtype', None)
        
        # returns patients list sorted by a requested keyword for appointment creation page on the front.
        if search_type == 'patient':
            keyword = self.request.query_params.get('q', None)
            
            if keyword:
                return self.queryset.filter(Q(user__email__icontains=keyword) | 
                                            Q(first_name__icontains=keyword) | 
                                            Q(last_name__icontains=keyword))
              
        # returns a object of a patient for patient information page on the front.
        else:
            email = self.request.query_params.get('email', None)
            user = CustomUser.objects.get(email=email)
            patient = self.queryset.filter(user=user)
            
            # To verify if the request.user is a manager or its own user(patient).
            if self.request.user.user_type != 'manager' and self.request.user.email != email:
                raise PermissionDenied('Wrong object owner')
            
            if not patient:
                Patient.objects.create(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name
                )
            return self.queryset.filter(user=user)
    

class DoctorViewSet(viewsets.ModelViewSet):
    
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        email = self.request.query_params.get('email', None)
        user = CustomUser.objects.get(email=email)
        doctor = self.queryset.filter(user=user)
        
        # To verify if the request.user is a manager or its own user(doctor).
        if self.request.user.user_type != 'manager' and self.request.user.email != email:
            raise PermissionDenied('Wrong object owner')
        
        if not doctor:
            Doctor.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name
            )
            print('created')

        return self.queryset.filter(user=user)
    

# since the queryset of above DoctorViewSet has been overridden,
# another apiview has to be defined separately for the doctors list.
class DoctorListAPIView(ListAPIView):
    
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    authentication_classes = []
    permissions = []
        
# to update doctor avatar separately
class DoctorPictureAPIView(UpdateAPIView):
    
    queryset = Doctor.objects.all()
    serializer_class = DoctorPictureSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
