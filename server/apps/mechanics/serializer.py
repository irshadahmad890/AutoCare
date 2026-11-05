from rest_framework import serializers
from .models import Mechanic, JobMechanic

class MechanicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mechanic
        fields = ['id', 'user', 'name', 'mechanic_type', 'phone_number', 'hourly_rate', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class JobMechanicSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobMechanic
        fields = ['id', 'job', 'mechanic', 'working_hours', 'assigned_at']
        read_only_fields = ['id']