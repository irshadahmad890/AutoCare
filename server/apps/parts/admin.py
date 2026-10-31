from django.contrib import admin
from .models import (Part, JobPart)

# Register your models here.
admin.site.register(Part)
admin.site.register(JobPart)