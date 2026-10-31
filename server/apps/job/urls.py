from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.jobs, name= 'jobs'),
    path('jobs/create', views.jobs_create, name= 'jobscreate'),
    path('jobs/update', views.jobs_update, name= 'jobsupdate'),
]

