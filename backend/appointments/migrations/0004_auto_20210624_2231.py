# Generated by Django 3.1.11 on 2021-06-24 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_auto_20210615_1751'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ['-date', '-timeslot']},
        ),
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together=set(),
        ),
    ]
