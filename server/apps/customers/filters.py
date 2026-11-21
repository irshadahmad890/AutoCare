import django_filters as filters
from .models import Customer

class CustomerFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(field_name='user__email', lookup_expr='icontains')
    phone = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'is_active']
