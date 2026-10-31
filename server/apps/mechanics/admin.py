from django.contrib import admin
from .models import (Mechanic, JobMechanic)

# Register your models here.
admin.site.register(Mechanic)
admin.site.register(JobMechanic)