# Generated by Django 3.1.11 on 2021-06-24 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210610_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('doctor', 'Doctor'), ('manager', 'Manager'), ('patient', 'Patient')], default='patient', max_length=60),
        ),
    ]
