from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from apps.customers.models import Customer
from .models import User

class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['role'] = user.role
        return token

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, validators=[validate_password])
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'name', 'address', 'role']
        read_only_fields = ['id', 'role']

    @transaction.atomic
    def create(self, validated_data):
        name = validated_data.pop('name')
        address = validated_data.pop('address', '')
        user = User.objects.create_user(**validated_data, role = 'customer')
        Customer.objects.create(user=user, name=name, phone=user.phone or '', address=address)
        return user

    def to_representation(self, instance):
        customer = instance.customer_profile
        return {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'role': instance.role,
            'name': customer.name,
            'phone': customer.phone,
            'address': customer.address
        }
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'first_name', 'last_name', 'role']
        read_only_fields = ['id', 'username', 'email', 'role']