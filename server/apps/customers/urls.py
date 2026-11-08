from django.urls import path
from . import views 

urlpatterns = [
    path("customer/", views.CustomerListCreateView.as_view(), name = 'customers'),
    path("customer/<int:pk>/", views.CustomerDetailView.as_view(), name = "customer_detail")
]
