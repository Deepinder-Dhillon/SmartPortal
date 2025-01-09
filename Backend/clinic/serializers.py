from rest_framework import serializers
from django.contrib.auth.models import User
from clinic.patient import Patient

class PatientSerializer(serializers.Serializer):
    phn = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    birth_date = serializers.CharField(max_length=15)
    phone = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    address = serializers.CharField(max_length=255)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {"password": {"write_only": True}}


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
