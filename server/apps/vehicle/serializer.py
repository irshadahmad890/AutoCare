from rest_framework import serializers
from .models import Vehicle
from apps.customers.models import Customer

class VehicleSerializer(serializers.ModelSerializer):

    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        required=False
    )

    class Meta:
        model = Vehicle
        fields = ['id','customer','make','model','year','registration_number','created_at','updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        user = self.context['request'].user
        is_admin = (
            getattr(user, 'role', None) == 'admin'
            or getattr(user, 'is_superuser', False)
        )

        if is_admin:
            if self.instance is None and not attrs.get('customer'):
                raise serializers.ValidationError({
                    'customer': 'Admin must provide a customer ID.'
                })
        else:
            customer = getattr(user, 'customer_profile', None)

            if customer is None:
                raise serializers.ValidationError(
                    'Customer profile does not exist.'
                )

            submitted_customer = attrs.get('customer')

            if submitted_customer and submitted_customer != customer:
                raise serializers.ValidationError({
                    'customer': 'You cannot assign a vehicle to another customer.'
                })

            attrs['customer'] = customer
        return attrs