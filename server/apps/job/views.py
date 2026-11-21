from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.common.pagination import StandardPagination
from apps.common.permissions import IsAdmin, IsAdminOrAssignedJobMechanic
from apps.user.models import Role
from .models import EstimateStatus, Job, JobMechanic, JobPart, JobStatus
from .serializer import (EstimateResponseSerializer, EstimateSerializer,
                         JobMechanicSerializer, JobPartSerializer, JobSerializer,
                         JobTransitionSerializer, SendEstimateSerializer)
from .services import respond_to_estimate, send_estimate, transition_job


def jobs_for_user(user):
    queryset = Job.objects.select_related('vehicle__customer').prefetch_related(
        'mechanic_assignments__mechanic', 'used_parts__part'
    )
    if not getattr(user, 'is_authenticated', False):
        return queryset.none()
    if user.role == Role.ADMIN:
        return queryset
    if user.role == Role.CUSTOMER:
        return queryset.filter(vehicle__customer__user=user)
    if user.role == Role.MECHANIC:
        return queryset.filter(mechanic_assignments__mechanic__user=user).distinct()
    return queryset.none()


@extend_schema(tags=['Jobs'])
class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'vehicle']
    ordering_fields = ['created_at', 'updated_at', 'job_number']

    def get_queryset(self):
        return jobs_for_user(self.request.user)

    def perform_create(self, serializer):
        if self.request.user.role != Role.ADMIN:
            raise PermissionDenied('Only Admin can create jobs.')
        serializer.save()


@extend_schema(tags=['Jobs'])
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return jobs_for_user(self.request.user)

    def perform_update(self, serializer):
        if self.request.user.role != Role.ADMIN:
            raise PermissionDenied('Only Admin can edit job details.')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != Role.ADMIN:
            raise PermissionDenied('Only Admin can delete jobs.')
        if instance.status not in [JobStatus.PENDING, JobStatus.CANCELLED]:
            raise ValidationError({'job': 'Only pending or cancelled jobs can be deleted.'})
        instance.delete()


@extend_schema(tags=['Jobs'])
class JobMechanicListCreateView(generics.ListCreateAPIView):
    serializer_class = JobMechanicSerializer
    permission_classes = [IsAdmin]
    pagination_class = StandardPagination

    def get_queryset(self):
        return JobMechanic.objects.select_related('job', 'mechanic', 'mechanic__user')


@extend_schema(tags=['Jobs'])
class JobMechanicDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobMechanic.objects.select_related('job', 'mechanic', 'mechanic__user')
    serializer_class = JobMechanicSerializer
    permission_classes = [IsAdmin]


def ensure_job_parts_editable(job):
    if hasattr(job, 'estimate') and job.estimate.status == EstimateStatus.APPROVED:
        raise ValidationError({'job': 'Parts cannot change after estimate approval.'})


@extend_schema(tags=['Jobs'])
class JobPartListCreateView(generics.ListCreateAPIView):
    serializer_class = JobPartSerializer
    permission_classes = [IsAdminOrAssignedJobMechanic]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['job', 'part']

    def get_queryset(self):
        queryset = JobPart.objects.select_related('job__estimate', 'part')
        if not getattr(self.request.user, 'is_authenticated', False):
            return queryset.none()
        if getattr(self.request.user, 'role', None) == Role.ADMIN:
            return queryset
        return queryset.filter(job__mechanic_assignments__mechanic__user=self.request.user).distinct()

    def perform_create(self, serializer):
        job = serializer.validated_data['job']
        ensure_job_parts_editable(job)
        if self.request.user.role == Role.MECHANIC and not job.mechanic_assignments.filter(mechanic__user=self.request.user).exists():
            raise PermissionDenied('You are not assigned to this job.')
        serializer.save()


@extend_schema(tags=['Jobs'])
class JobPartDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobPartSerializer
    permission_classes = [IsAdminOrAssignedJobMechanic]

    def get_queryset(self):
        queryset = JobPart.objects.select_related('job__estimate', 'part')
        if self.request.user.role == Role.ADMIN:
            return queryset
        return queryset.filter(job__mechanic_assignments__mechanic__user=self.request.user).distinct()

    def perform_update(self, serializer):
        ensure_job_parts_editable(serializer.instance.job)
        serializer.save()

    def perform_destroy(self, instance):
        ensure_job_parts_editable(instance.job)
        instance.delete()


class SendEstimateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(tags=['Estimates'], request=SendEstimateSerializer, responses={200: EstimateSerializer})
    def post(self, request, job_pk):
        job = get_object_or_404(Job, pk=job_pk)
        serializer = SendEstimateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(EstimateSerializer(send_estimate(job.pk, serializer.validated_data.get('notes', ''))).data)


class EstimateDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Estimates'], request=EstimateResponseSerializer, responses={200: EstimateSerializer})
    def get(self, request, job_pk):
        job = get_object_or_404(jobs_for_user(request.user).select_related('estimate'), pk=job_pk)
        if not hasattr(job, 'estimate'):
            raise ValidationError({'estimate': 'No estimate exists for this job.'})
        return Response(EstimateSerializer(job.estimate).data)


class EstimateResponseView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EstimateResponseSerializer

    @extend_schema(tags=['Estimates'], responses={200: EstimateSerializer})
    def post(self, request, job_pk):
        if request.user.role != Role.CUSTOMER:
            raise PermissionDenied('Only the job customer can respond to an estimate.')
        serializer = EstimateResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(EstimateSerializer(respond_to_estimate(job_pk, request.user, serializer.validated_data['approve'])).data)


class JobTransitionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Jobs'], request=JobTransitionSerializer, responses={200: JobSerializer})
    def post(self, request, pk):
        job = get_object_or_404(jobs_for_user(request.user), pk=pk)
        if request.user.role not in [Role.ADMIN, Role.MECHANIC]:
            raise PermissionDenied('Only Admin or an assigned mechanic can transition a job.')
        serializer = JobTransitionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(JobSerializer(transition_job(job.pk, serializer.validated_data['status'])).data)
