# Generated by Django 3.1.11 on 2021-06-15 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usertypes', '0009_auto_20210614_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('timeslot', models.SmallIntegerField(choices=[(0, '09:00'), (1, '09:15'), (2, '09:30'), (3, '09:45'), (4, '10:00'), (5, '10:15'), (6, '10:30'), (7, '10:45'), (8, '11:00'), (9, '11:15'), (10, '11:30'), (11, '11:45'), (12, '12:00'), (13, '12:15'), (14, '12:30'), (15, '12:45'), (16, '14:00'), (17, '14:15'), (18, '14:30'), (19, '14:45'), (20, '15:00'), (21, '15:15'), (22, '15:30'), (23, '15:45'), (24, '16:00'), (25, '16:15'), (26, '16:30'), (27, '16:45'), (28, '17:00'), (29, '17:15'), (30, '17:30'), (31, '17:45')])),
                ('is_available', models.BooleanField(default=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='usertypes.doctor')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='appointments', to='usertypes.patient')),
            ],
            options={
                'unique_together': {('doctor', 'patient', 'date', 'timeslot')},
            },
        ),
    ]
