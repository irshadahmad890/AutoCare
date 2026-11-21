from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from .models import Part
from .serializer import PartSerializer
from apps.common.permissions import IsAdmin
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Inventory'])
class PartListCreateView(ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAdmin]

@extend_schema(tags=['Inventory'])
class PartDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAdmin]
