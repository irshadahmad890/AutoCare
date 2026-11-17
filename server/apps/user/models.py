from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    CUSTOMER = "customer", "Customer"
    MECHANIC = "mechanic", "Mechanic"

class User(AbstractUser):

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        self.email = (self.email or "").strip().lower()
        self.phone = (self.phone or "").strip() or None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email