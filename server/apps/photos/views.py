from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from apps.common.pagination import StandardPagination
from apps.user.models import Role
from .models import RepairPhoto
from .serializers import RepairPhotoSerializer


class RepairPhotoListCreateView(generics.ListCreateAPIView):
    serializer_class = RepairPhotoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['job']

    def get_queryset(self):
        queryset = RepairPhoto.objects.select_related('job__vehicle__customer', 'uploaded_by')
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        if getattr(user, 'role', None) == Role.ADMIN:
            return queryset
        if user.role == Role.MECHANIC:
            return queryset.filter(job__mechanic_assignments__mechanic__user=user).distinct()
        if user.role == Role.CUSTOMER:
            return queryset.filter(job__vehicle__customer__user=user)
        return queryset.none()

    def perform_create(self, serializer):
        user = self.request.user
        job = serializer.validated_data['job']
        if user.role == Role.MECHANIC and job.mechanic_assignments.filter(mechanic__user=user).exists():
            serializer.save(uploaded_by=user)
            return
        if user.role == Role.ADMIN:
            serializer.save(uploaded_by=user)
            return
        raise PermissionDenied('Only Admin or an assigned mechanic can upload repair photos.')


class RepairPhotoDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = RepairPhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RepairPhotoListCreateView.get_queryset(self)

    def perform_destroy(self, instance):
        if self.request.user.role != Role.ADMIN and instance.uploaded_by_id != self.request.user.id:
            raise PermissionDenied('You can only delete photos you uploaded.')
        instance.image.delete(save=False)
        instance.delete()
