import re
from rest_framework import serializers
from apps.user.models import Role
from .models import Customer

PHONE_RE = re.compile(r"^\+?[0-9][0-9\s-]{6,14}$")

class CustomerValidationMixin:
    def validate_name(self, value):
        value = " ".join(value.split())
        if len(value) < 2:
            raise serializers.ValidationError("Enter the full name.")
        return value

    def validate_phone(self, value):
        value = (value or "").strip()
        if value and not PHONE_RE.match(value):
            raise serializers.ValidationError("Enter a valid phone number, for example 03001234567.")
        return value

class CustomerSerializer(CustomerValidationMixin, serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'user', 'name', 'phone', 'address', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'vehicle_count', 'user', 'created_at', 'updated_at']

    def validate_user(self, user):
        if user is not None and user.role != Role.CUSTOMER:
            raise serializers.ValidationError("Only a user with the customer role can be linked.")
        return user

class CustomerSelfSerializer(CustomerValidationMixin, serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
