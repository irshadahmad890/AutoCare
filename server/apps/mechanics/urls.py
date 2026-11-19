from django.urls import path
from .views import (
    SpecializationListCreateView,
    SpecializationDetailView,
    MechanicListCreateView,
    MechanicDetailView,
)

urlpatterns = [
    path('specializations/', SpecializationListCreateView.as_view(), name = 'specialization-list-create'),
    path('specializations/<int:pk>/', SpecializationDetailView.as_view(), name = 'specialization-detail'),
    path('', MechanicListCreateView.as_view(), name = 'mechanic-list-create'),
    path('<int:pk>/', MechanicDetailView.as_view(), name = 'mechanic-detail'),
]
