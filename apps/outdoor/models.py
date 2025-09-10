from django.db import models
from django.utils.timezone import now


class OutdoorActivity(models.Model):
    title = models.CharField(max_length=150, help_text="Enter the place of activity.")
    category = models.CharField(max_length=255, default='other')
    latitude = models.FloatField()
    longitude= models.FloatField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = "Outdoor activities"
        ordering = ['title']
        #constraints = [
        #    models.UniqueConstraint(fields=['', 'activity'], name='unique_activity_per_name')
        #]