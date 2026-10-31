from django.db import models
from apps.job.models import Job
from django.core.validators import MinValueValidator

# Create your models here.
class Part(models.Model):

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class JobPart(models.Model):

    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name='used_parts')
    part = models.ForeignKey(Part,on_delete=models.PROTECT,related_name='job_usages')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.part.name} - {self.quantity}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['job', 'part'],
                name='unique_job_part'
            )
        ]
