from rest_framework import generics
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from apps.common.permissions import IsAdmin, IsCustomer
from .models import Customer
from .serializer import CustomerSerializer, CustomerSelfSerializer
from .filters import CustomerFilter

@extend_schema(tags=['Customers'])
class CustomerListCreateView(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAdmin]
    filterset_class = CustomerFilter
    search_fields = ['name', 'phone', 'address', 'user__email']
    ordering_fields = ['name', 'created_at']

@extend_schema(tags=['Customers'])
class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAdmin]
    

@extend_schema(tags=['Customers'])
class CustomerProfileView(APIView):
    serializer_class = CustomerSelfSerializer
    permission_classes = [IsCustomer]

    def get_customer(self):
        return get_object_or_404(Customer, user=self.request.user)

    def get(self, request):
        serializer = self.serializer_class(self.get_customer())
        return Response(serializer.data)
