from .models import Vehicle
from .serializer import VehicleSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from apps.common.permissions import IsCustomerOrAdmin, VehiclePermissions
from rest_framework.exceptions import ValidationError
from apps.user.models import User, Role
from apps.customers.models import Customer

class VehicleListCreateView(ListCreateAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [IsCustomerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, User):
            if user.role == Role.ADMIN:
                return Vehicle.objects.all()
            if user.role == Role.CUSTOMER:
                return Vehicle.objects.filter(customer__user=user)
        return Vehicle.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if isinstance(user, User):
            if user.role == Role.ADMIN:
                if not serializer.validated_data.get('customer'):
                    raise ValidationError({
                        'customer': 'Please select a customer.'
                    })
                serializer.save()
            elif user.role == Role.CUSTOMER:
                try:
                    customer = user.customer_profile
                except Customer.DoesNotExist:
                    raise ValidationError({
                        'customer': 'Customer profile does not exist.'
                    })
                serializer.save(customer = customer)

class VehicleDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [IsCustomerOrAdmin, VehiclePermissions]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, User):
            if user.role == Role.ADMIN:
                return Vehicle.objects.all()
            if user.role == Role.CUSTOMER:
                return Vehicle.objects.filter(customer__user=user)
        return Vehicle.objects.none()

    def perform_update(self, serializer):
        user = self.request.user
        if isinstance(user, User) and user.role == Role.CUSTOMER:
            customer = user.customer_profile
            serializer.save(customer=customer)
        else:
            serializer.save()