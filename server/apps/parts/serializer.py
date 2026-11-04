from rest_framework import serializers
from .models import Part, JobPart


class PartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Part
        fields = ['id', 'name', 'price', 'stock', 'created_at']
        read_only_fields = ['id', 'created_at']

class JobPartSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobPart
        fields = ['id', 'job', 'part', 'quantity', 'unit_price']
        read_only_fields = ['id']