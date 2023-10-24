from django.contrib.auth import get_user_model
from rest_framework import serializers
from users import services as user_services

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = user_services.create_user(**validated_data)
        return user
