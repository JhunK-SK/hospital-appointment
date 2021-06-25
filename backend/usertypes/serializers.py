from accounts.serializers import CustomUserSerializer
from rest_framework import serializers

from .models import Doctor, Patient


class PatientSerializer(serializers.ModelSerializer):
    
    user = CustomUserSerializer()
        
    class Meta:
        model = Patient
        fields = (
            'id',
            'user',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'height',
            'weight',
            'insurance_number',
            'address1',
            'address2',
            'city',
            'state',
            'is_filled_in'
        )
    
    # By updating patient model, common fields such as first name and last name 
    # will be updated in the CustomUser model as well.
    def update(self, instance, validated_data):
        first_name = validated_data.get('first_name', instance.first_name)
        last_name = validated_data.get('last_name', instance.last_name)
        user = instance.user
        user.first_name = first_name
        user.last_name = last_name
        user.user_type = validated_data.get('user', instance.user).get('user_type', instance.user.user_type)
        user.save()
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.height = validated_data.get('height', instance.height)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.insurance_number = validated_data.get('insurance_number', instance.insurance_number)
        instance.address1 = validated_data.get('address1', instance.address1)
        instance.address2 = validated_data.get('address2', instance.address2)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.is_filled_in = validated_data.get('is_filled_in', instance.is_filled_in)
        instance.save()
        
        return instance
    
    
class DoctorSerializer(serializers.ModelSerializer):
    
    user = CustomUserSerializer()
    picture = serializers.ImageField(read_only=True)
    
    class Meta:
        model = Doctor
        fields = (
            'id',
            'user',
            'first_name',
            'last_name',
            'specialty',
            'picture',
        )
        
    
    def update(self, instance, validated_data):
        first_name = validated_data.get('first_name', instance.first_name)
        last_name = validated_data.get('last_name', instance.last_name)
        user = instance.user
        user.first_name = first_name
        user.last_name = last_name
        user.user_type = validated_data.get('user', instance.user).get('user_type', instance.user.user_type)
        user.save()
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.specialty = validated_data.get('specialty', instance.specialty)
        instance.save()
        
        return instance


class DoctorPictureSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Doctor
        read_only_fields = (
            'id',
            'user',
            'first_name',
            'last_name',
            'specialty',
        )
        fields = (
            'picture',
        )
