import django_filters as filters
from .models import Customer

class CustomerFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    phone = filters.CharFilter(lookup_expr='icontains')
    has_account = filters.BooleanFilter(field_name='user', lookup_expr='isnull', exclude=True)

    class Meta:
        model = Customer
        fields = ['is_active']
