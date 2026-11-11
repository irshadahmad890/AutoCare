from .models import Vehicle
from .serializer import VehicleSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated

class VehicleListCreateView(ListCreateAPIView):

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if (
            getattr(user, 'role', None) == 'admin'
            or getattr(user, 'is_superuser', False)
        ):
            return Vehicle.objects.all()

        return Vehicle.objects.filter(customer__user=user)


class VehicleDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if (
            getattr(user, 'role', None) == 'admin'
            or getattr(user, 'is_superuser', False)
        ):
            return Vehicle.objects.all()

        return Vehicle.objects.filter(customer__user=user)