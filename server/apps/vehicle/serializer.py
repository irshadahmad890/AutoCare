from rest_framework import serializers 
from models import Vehicle

class VehiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        feilds = ['customer', 'make', 'model', 'year', 'registration_number']

