from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Part(models.Model):

    name = models.CharField(max_length=100, unique = True)
    part_number = models.CharField(max_length = 50, unique = True)
    price = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'id']