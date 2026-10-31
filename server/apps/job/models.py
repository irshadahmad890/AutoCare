from django.db import models
from apps.vehicle.models import Vehicle

# Create your models here.

class Job(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    job_number = models.CharField(max_length=30,unique=True)
    vehicle = models.ForeignKey(Vehicle ,on_delete=models.PROTECT,related_name='jobs')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job_number

    class Meta:
        ordering = ['-created_at']