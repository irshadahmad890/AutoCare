
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated

from .models import Customer
from .serializer import CustomerSerializer


class CustomerListCreateView(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    # type: ignore[override]
    def get_queryset(self):
        user = self.request.user

        if (
            getattr(user, 'role', None) == 'admin'
            or getattr(user, 'is_superuser', False)
        ):
            return Customer.objects.all()

        return Customer.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomerDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    # type: ignore[override]
    def get_queryset(self):
        user = self.request.user

        if (
            getattr(user, 'role', None) == 'admin'
            or getattr(user, 'is_superuser', False)
        ):
            return Customer.objects.all()

        return Customer.objects.filter(user=user)
