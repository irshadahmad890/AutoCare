from django.urls import path

from .views import RepairPhotoDetailView, RepairPhotoListCreateView

urlpatterns = [
    path('', RepairPhotoListCreateView.as_view(), name='repair-photo-list-create'),
    path('<int:pk>/', RepairPhotoDetailView.as_view(), name='repair-photo-detail'),
]
