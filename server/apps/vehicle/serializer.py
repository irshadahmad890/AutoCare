from rest_framework import serializers
from .models import Vehicle
from apps.customers.models import Customer

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['id','customer','make','model','year','registration_number','created_at','updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {'customer': {'required': False}}