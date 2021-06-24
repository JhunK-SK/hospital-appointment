from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DoctorListAPIView, DoctorPictureAPIView, DoctorViewSet,
                    PatientViewSet)

router = DefaultRouter()
router.register('patients', PatientViewSet, basename='patients')
router.register('doctors', DoctorViewSet, basename='doctors')

urlpatterns = [
    path('', include(router.urls)),
    path('doctor-list/', DoctorListAPIView.as_view(), name='doctor-list'),
    path('doctor-picture/<int:pk>/', DoctorPictureAPIView.as_view(), name='doctor-picture'),
]
