from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListCreateView.as_view(), name='job_list_create'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('<int:pk>/transition/', views.JobTransitionView.as_view(), name='job-transition'),
    path('<int:job_pk>/estimate/', views.EstimateDetailView.as_view(), name='estimate-detail'),
    path('<int:job_pk>/estimate/send/', views.SendEstimateView.as_view(), name='estimate-send'),
    path('<int:job_pk>/estimate/respond/', views.EstimateResponseView.as_view(), name='estimate-respond'),
    path('assign-mechanic/', views.JobMechanicListCreateView.as_view(), name = 'job-mechanic-list-create'),
    path('assign-mechanic/<int:pk>/', views.JobMechanicDetailView.as_view(), name = 'job-mechanic-detail'),
    path("job-parts/", views.JobPartListCreateView.as_view(), name="job_part_list_add"),
    path("job-parts/<int:pk>/", views.JobPartDetailView.as_view(), name="job_part_detail")
]
