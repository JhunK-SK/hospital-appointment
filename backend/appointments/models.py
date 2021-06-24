from django.db import models
from django.db.models.fields import TextField
from usertypes.models import Doctor, Patient


class Appointment(models.Model):
    
    class Meta:
        unique_together = ('doctor', 'date', 'timeslot')
    
    TIMESLOT_LIST = (
        (0, '09:00'), (1, '09:15'), (2, '09:30'), (3, '09:45'),
        (4, '10:00'), (5, '10:15'), (6, '10:30'), (7, '10:45'),
        (8, '11:00'), (9, '11:15'), (10, '11:30'), (11, '11:45'),
        (12, '12:00'), (13, '12:15'), (14, '12:30'), (15, '12:45'),
        (16, '14:00'), (17, '14:15'), (18, '14:30'), (19, '14:45'),
        (20, '15:00'), (21, '15:15'), (22, '15:30'), (23, '15:45'),
        (24, '16:00'), (25, '16:15'), (26, '16:30'), (27, '16:45'),
        (28, '17:00'), (29, '17:15'), (30, '17:30'), (31, '17:45'),
    )
    
    doctor = models.ForeignKey(Doctor, related_name='appointments', 
                               on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, blank=True, null=True, 
                                related_name='appointments', 
                                on_delete=models.PROTECT)
    date = models.DateField()
    timeslot = models.SmallIntegerField(choices=TIMESLOT_LIST)
    is_available = models.BooleanField(default=True)
    symptom = TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date', '-timeslot']
    
    def __str__(self):
        return f'{self.time} - {self.date} - doctor: {self.doctor} patient: {self.patient}'
    
    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]
