from rest_framework import serializers
from .models import Part


class PartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Part
        fields = ['id', 'name', 'part_number', 'price', 'stock', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at']