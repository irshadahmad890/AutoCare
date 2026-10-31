from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def jobs(request):
    return HttpResponse('Here is all jobs!')

def jobs_create(request):
    return HttpResponse('Here is all jobs!')

def jobs_update(request):
    return HttpResponse('Here is all jobs!')
