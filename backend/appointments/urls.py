from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AppointmentListAPIView, AppointmentViewSet

router = DefaultRouter()
router.register('appointments', AppointmentViewSet, basename='appointments')

urlpatterns = [
    path('', include(router.urls)),
    path('appointment-timeslots/', AppointmentListAPIView.as_view(), 
         name='appointment-timeslots'),
]
