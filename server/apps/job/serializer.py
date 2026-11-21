from rest_framework import serializers
from .models import Job, JobMechanic, JobPart

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'job_number', 'vehicle', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'job_number', 'created_at', 'updated_at']

class JobMechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobMechanic
        fields = ['id', 'job', 'mechanic', 'working_hours', 'assigned_at', 'updated_at']
        read_only_fields = ['id', 'assigned_at', 'updated_at']

class JobPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPart
        fields = ['id', 'job', 'part', 'quantity', 'unit_price', 'added_at', 'updated_at']
        read_only_fields = ['id','job','unit_price','added_at','updated_at']

    def validate(self, attrs):
        part = attrs.get('part', self.instance.part if self.instance else None)
        quantity = attrs.get('quantity', self.instance.quantity if self.instance else None)
        if part and quantity and quantity > part.stock:
            raise serializers.ValidationError({
                'quantity': 'Insufficient stock available.'
            })

        return attrs
    
    def create(self, validated_data):
        validated_data['unit_price'] = validated_data['part'].price
        return super().create(validated_data)