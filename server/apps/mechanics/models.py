from django.db import models
from apps.job.models import Job
from django.conf import settings

# Create your models here.
class Mechanic(models.Model):

    TYPE_CHOICES = [
        ('senior', 'Senior'),
        ('junior', 'Junior'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='mechanic_profile',null=True,blank=True)
    name = models.CharField(max_length=100)
    mechanic_type = models.CharField(max_length=20,choices=TYPE_CHOICES)
    phone_number = models.CharField(max_length=20)
    hourly_rate = models.DecimalField(max_digits=10,decimal_places=2)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class JobMechanic(models.Model):

    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name='mechanic_assignments')
    mechanic = models.ForeignKey(Mechanic,on_delete=models.PROTECT,related_name='job_assignments')
    working_hours = models.DecimalField(max_digits=5,decimal_places=2)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mechanic.name} - {self.job.job_number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['job', 'mechanic'],
                name='unique_job_mechanic'
            )
        ]

