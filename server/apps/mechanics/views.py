
from rest_framework import generics
from .models import Mechanic, JobMechanic, Specialization
from .serializer import (
    MechanicSerializer,
    MechanicCreateSerializer,
    JobMechanicSerializer,
    SpecializationSerializer
)
from .permissions import IsAdminRole, IsAdminOrOwnMechanic, IsAdminOrAssignedMechanic

class SpecializationListCreateView(generics.ListCreateAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAdminRole]

class SpecializationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAdminRole]



class MechanicListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrOwnMechanic]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_superuser:
            return Mechanic.objects.select_related('user', 'specialization').all()
        return Mechanic.objects.select_related('user', 'specialization').filter(user = user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MechanicCreateSerializer
        return MechanicSerializer


class MechanicDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MechanicSerializer
    permission_classes = [IsAdminOrOwnMechanic]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_superuser:
            return Mechanic.objects.select_related('user', 'specialization').all()
        return Mechanic.objects.select_related('user', 'specialization').filter(user = user)


# Job Mechanic APIs

class JobMechanicListCreateView(generics.ListCreateAPIView):
    serializer_class = JobMechanicSerializer
    permission_classes = [IsAdminOrAssignedMechanic]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_superuser:
            return JobMechanic.objects.select_related('job', 'mechanic', 'mechanic__user').all()
        return JobMechanic.objects.select_related('job', 'mechanic', 'mechanic__user').filter(mechanic__user = user)


class JobMechanicDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobMechanicSerializer
    permission_classes = [IsAdminOrAssignedMechanic]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_superuser:
            return JobMechanic.objects.select_related('job', 'mechanic', 'mechanic__user').all()
        return JobMechanic.objects.select_related('job', 'mechanic', 'mechanic__user').filter(mechanic__user = user)
