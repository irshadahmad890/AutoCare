from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)
from apps.customers.models import Customer

# Create your models here.
class Vehicle(models.Model):

    customer = models.ForeignKey(Customer,on_delete=models.PROTECT,related_name='vehicles')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100)
        ]
    )
    registration_number = models.CharField(max_length=20,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.make} {self.model} - {self.registration_number}"

    class Meta:
        ordering = ['-created_at']
