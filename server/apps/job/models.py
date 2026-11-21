from django.db import models, transaction
from django.core.validators import MinValueValidator
from apps.vehicle.models import Vehicle
from apps.mechanics.models import Mechanic
from apps.parts.models import Part

class JobStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'

class Job(models.Model):
    job_number = models.CharField(max_length = 30, unique = True, null = True, blank = True, editable = False)
    vehicle = models.ForeignKey(Vehicle, on_delete = models.PROTECT, related_name = 'jobs')
    description = models.TextField(blank = True)
    status = models.CharField(max_length = 20, choices = JobStatus.choices, default = JobStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.job_number:
            self.job_number = f"JOB-{self.created_at.year}-{self.pk:06d}"
            type(self).objects.filter(pk = self.pk).update(job_number = self.job_number)

    def __str__(self):
        return self.job_number or f"Job {self.pk}"

    class Meta:
        ordering = ['-created_at', 'id']

class JobMechanic(models.Model):
    job = models.ForeignKey(Job, on_delete = models.CASCADE, related_name = 'mechanic_assignments')
    mechanic = models.ForeignKey(Mechanic, on_delete = models.PROTECT, related_name = 'job_assignments')
    working_hours = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0, validators = [MinValueValidator(0)])
    assigned_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.mechanic.name} - {self.job.job_number}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['job', 'mechanic'], name = 'unique_job_mechanic')
        ]

class JobPart(models.Model):
    job = models.ForeignKey(Job, on_delete = models.CASCADE, related_name = 'used_parts')
    part = models.ForeignKey(Part, on_delete = models.PROTECT, related_name = 'job_usages')
    quantity = models.PositiveIntegerField(validators = [MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(0)])
    added_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.part.name} - {self.quantity}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['job', 'part'], name = 'unique_job_part')
        ]