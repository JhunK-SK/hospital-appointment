from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

User = get_user_model()

class CustomUserCreateSerializer(UserCreateSerializer):
    
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'password', 'first_name', 'last_name',)
        

class CustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        read_only_fields = ('email', 'id', 'date_joined',)
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'user_type',
            'get_joined_data_formatted',
            'get_full_name',
        )
