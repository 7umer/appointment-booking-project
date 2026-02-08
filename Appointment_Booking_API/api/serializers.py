from rest_framework import serializers
from django.conf import settings
from .models import User, Appointment

# ----------------------
# User serializers
# ----------------------
class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'avatar']

    def get_avatar(self, obj):
        if obj.avatar:
            return settings.BASE_URL + obj.avatar.url
        return None

class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'avatar']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# ----------------------
# Appointment serializer
# ----------------------
class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id',
            'name',
            'patient_name',
            'phone',
            'email',
            'service',
            'date',
            'message',
            'status',
            'created_at',
        ]
        read_only_fields = ['status', 'created_at']
