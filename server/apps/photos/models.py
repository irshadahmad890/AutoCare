from django.conf import settings
from django.db import models

from apps.job.models import Job


class RepairPhoto(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='photos')
    image = models.FileField(upload_to='repair_photos/%Y/%m/%d/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='repair_photos')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-id']
