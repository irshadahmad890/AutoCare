from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.exceptions import PermissionDenied
from .models import Job, JobMechanic, JobPart
from .serializer import (
    JobSerializer,
    JobMechanicSerializer,
    JobPartSerializer
)
from apps.common.permissions import IsAdmin, IsAdminOrAssignedJobMechanic
from apps.user.models import Role
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Jobs'])
class JobListCreateView(ListCreateAPIView):
    queryset = Job.objects.select_related('vehicle')
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]

@extend_schema(tags=['Jobs'])
class JobDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.select_related('vehicle')
    serializer_class = JobSerializer
    permission_classes = [IsAdmin]

@extend_schema(tags=['Jobs'])
class JobMechanicListCreateView(ListCreateAPIView):
    serializer_class = JobMechanicSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return JobMechanic.objects.select_related(
            'job', 'mechanic', 'mechanic__user'
        )

@extend_schema(tags=['Jobs'])
class JobMechanicDetailView(RetrieveUpdateDestroyAPIView):
    queryset = JobMechanic.objects.select_related(
        'job', 'mechanic', 'mechanic__user'
    )
    serializer_class = JobMechanicSerializer
    permission_classes = [IsAdmin]

@extend_schema(tags=['Jobs'])
class JobPartListCreateView(ListCreateAPIView):
    serializer_class = JobPartSerializer
    permission_classes = [IsAdminOrAssignedJobMechanic]

    def get_queryset(self):
        user = self.request.user
        queryset = JobPart.objects.select_related('job', 'part')
        if user.role == Role.ADMIN:
            return queryset
        return queryset.filter(
            job__mechanic_assignments__mechanic__user = user
        ).distinct()

    def perform_create(self, serializer):
        user = self.request.user
        job = serializer.validated_data['job']
        if user.role == Role.MECHANIC:
            is_assigned = job.mechanic_assignments.filter(mechanic__user = user).exists()
            if not is_assigned:
                raise PermissionDenied("You are not assigned to this job.")
        serializer.save()

@extend_schema(tags=['Jobs'])
class JobPartDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = JobPartSerializer
    permission_classes = [IsAdminOrAssignedJobMechanic]

    def get_queryset(self):
        user = self.request.user
        queryset = JobPart.objects.select_related('job', 'part')
        if user.role == Role.ADMIN:
            return queryset
        return queryset.filter(
            job__mechanic_assignments__mechanic__user = user
        ).distinct()
