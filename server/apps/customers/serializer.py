from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'user','name', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']