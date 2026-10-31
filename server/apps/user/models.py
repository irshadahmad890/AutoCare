from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('mechanic', 'Mechanic'),
        ('staff', 'Staff'),
    ]
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,unique=True,null=True,blank=True)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='customer')

    def __str__(self):
        return self.email