from rest_framework import serializers
from .models import Estimate, Job, JobMechanic, JobPart, JobStatus

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'job_number', 'vehicle', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'job_number', 'status', 'created_at', 'updated_at']

    def validate_status(self, value):
        # Stage changes are handled by the dedicated transition endpoint.
        if self.instance and value != self.instance.status:
            raise serializers.ValidationError('Use the job transition endpoint to change status.')
        return value


class EstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = ['id', 'job', 'status', 'notes', 'sent_at', 'responded_at',
                  'approved_by', 'stock_deducted', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'sent_at', 'responded_at', 'approved_by',
                            'stock_deducted', 'created_at', 'updated_at']


class SendEstimateSerializer(serializers.Serializer):
    notes = serializers.CharField(required=False, allow_blank=True)


class EstimateResponseSerializer(serializers.Serializer):
    approve = serializers.BooleanField()


class JobTransitionSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=JobStatus.choices)

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
        return attrs
    
    def create(self, validated_data):
        validated_data['unit_price'] = validated_data['part'].price
        return super().create(validated_data)
