from django.urls import path
from .views import (
    SpecializationListCreateView,
    SpecializationDetailView,
    MechanicListCreateView,
    MechanicDetailView,
    JobMechanicListCreateView,
    JobMechanicDetailView
)

urlpatterns = [
    path('specializations/', SpecializationListCreateView.as_view(), name = 'specialization-list-create'),
    path('specializations/<int:pk>/', SpecializationDetailView.as_view(), name = 'specialization-detail'),
    path('', MechanicListCreateView.as_view(), name = 'mechanic-list-create'),
    path('<int:pk>/', MechanicDetailView.as_view(), name = 'mechanic-detail'),
    path('assignments/', JobMechanicListCreateView.as_view(), name = 'job-mechanic-list-create'),
    path('assignments/<int:pk>/', JobMechanicDetailView.as_view(), name = 'job-mechanic-detail'),
]
