# Generated by Django 3.1.11 on 2021-06-11 14:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usertypes', '0004_auto_20210611_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]
