from rest_framework import generics
from .models import Mechanic, Specialization
from .serializer import (
    MechanicSerializer,
    MechanicCreateSerializer,
    SpecializationSerializer
)
from apps.common.permissions import IsAdmin, IsAdminOrOwnMechanic
from apps.user.models import User, Role
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Mechanics'])
class SpecializationListCreateView(generics.ListCreateAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAdmin]

@extend_schema(tags=['Mechanics'])
class SpecializationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAdmin]

@extend_schema(tags=['Mechanics'])
class MechanicListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrOwnMechanic]

    def get_queryset(self):
        user = self.request.user
        queryset = Mechanic.objects.select_related('user', 'specialization')
        if isinstance(user, User):
            if user.role == Role.ADMIN:
                return queryset.all()
            if user.role == Role.MECHANIC:
                return queryset.filter(user = user)
        return queryset.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MechanicCreateSerializer
        return MechanicSerializer


@extend_schema(tags=['Mechanics'])
class MechanicDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MechanicSerializer
    permission_classes = [IsAdminOrOwnMechanic]

    def get_queryset(self):
        user = self.request.user
        queryset = Mechanic.objects.select_related('user', 'specialization')
        if isinstance(user, User):
            if user.role == Role.ADMIN:
                return queryset.all()
            if user.role == Role.MECHANIC:
                return queryset.filter(user = user)
        return queryset.none()
