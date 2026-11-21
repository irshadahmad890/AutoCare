from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from .models import Part
from .serializer import PartSerializer
from apps.common.permissions import IsAdmin
from drf_spectacular.utils import extend_schema
from apps.common.pagination import StandardPagination
from django_filters.rest_framework import DjangoFilterBackend

@extend_schema(tags=['Inventory'])
class PartListCreateView(ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAdmin]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'part_number']
    search_fields = ['name', 'part_number']
    ordering_fields = ['name', 'stock', 'price', 'created_at']

@extend_schema(tags=['Inventory'])
class PartDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAdmin]
