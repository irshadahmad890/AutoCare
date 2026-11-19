from django.urls import path
from .views import PartListCreateView, PartDetailView

urlpatterns = [
    path("", PartListCreateView.as_view(), name= "part_list_create"),
    path("<int:pk>/", PartDetailView.as_view(), name= "part_detail")
]
