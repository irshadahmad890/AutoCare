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
from drf_spectacular.utils import extend_schema
from apps.common.pagination import StandardPagination
from django_filters.rest_framework import DjangoFilterBackend

@extend_schema(tags=['Vehicles'])
class VehicleListCreateView(ListCreateAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [IsCustomerOrAdmin]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['make', 'model', 'year', 'customer']
    ordering_fields = ['created_at', 'year', 'registration_number']

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, User):
            if user.role == Role.ADMIN:
                return Vehicle.objects.select_related('customer__user')
            if user.role == Role.CUSTOMER:
                return Vehicle.objects.select_related('customer__user').filter(customer__user=user)
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

@extend_schema(tags=['Vehicles'])
class VehicleDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [IsCustomerOrAdmin, VehiclePermissions]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, User):
            if user.role == Role.ADMIN:
                return Vehicle.objects.select_related('customer__user')
            if user.role == Role.CUSTOMER:
                return Vehicle.objects.select_related('customer__user').filter(customer__user=user)
        return Vehicle.objects.none()

    def perform_update(self, serializer):
        user = self.request.user
        if isinstance(user, User) and user.role == Role.CUSTOMER:
            customer = user.customer_profile
            serializer.save(customer=customer)
        else:
            serializer.save()
