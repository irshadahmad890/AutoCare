from apps.job.models import Job
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

class Specialization(models.Model):

    name = models.CharField(max_length = 100, unique = True)
    description = models.TextField(blank = True)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Mechanic(models.Model):

    EXPERIENCE_LEVEL_CHOICES = [
        ('junior', 'Junior'),
        ('senior', 'Senior'),
        ('expert', 'Expert')
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'mechanic_profile')
    specialization = models.ForeignKey(Specialization, on_delete = models.PROTECT, related_name = 'mechanics', null = True)
    name = models.CharField(max_length = 100)
    experience_level = models.CharField(max_length = 20, choices = EXPERIENCE_LEVEL_CHOICES, default = 'Junior')
    hourly_rate = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(0)])
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

class JobMechanic(models.Model):

    job = models.ForeignKey(Job, on_delete = models.CASCADE, related_name = 'mechanic_assignments')
    mechanic = models.ForeignKey(Mechanic, on_delete = models.PROTECT, related_name = 'job_assignments')
    working_hours = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0, validators = [MinValueValidator(0)])
    assigned_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.mechanic.name} - {self.job.job_number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['job', 'mechanic'],
                name = 'unique_job_mechanic'
            )
        ]
