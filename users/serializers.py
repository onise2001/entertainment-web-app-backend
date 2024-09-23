from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser



class CustomTokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password) 

        if user is None:
            raise serializers.ValidationError('Invalid Credentials')
        

        refresh = RefreshToken.for_user(user)

        update_last_login(None, user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs  = { 'password': {"read_only": True }}

    
    def create(self,validated_data):
        user = CustomUser.create_user(**validated_data)
        user.save()
        return user