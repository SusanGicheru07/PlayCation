from django.db import models

class OutdoorLocation(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Outdoor locations"
        ordering = ['name']


class OutdoorActivity(models.Model):
    ACTIVITY_TYPES = [
        ('hike', 'Hike Trail'),
        ('camping', 'Camping'),
        ('picnic', 'Picnic Area'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=150, help_text="Enter the place of activity.")
    activity = models.CharField(max_length=50, choices=ACTIVITY_TYPES, default='other')
    lat = models.FloatField()
    lng = models.FloatField()
    location = models.ForeignKey(OutdoorLocation, on_delete=models.CASCADE, related_name='activities')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.get_activity_display()}"

    class Meta:
        verbose_name_plural = "Outdoor activities"
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'activity'], name='unique_activity_per_name')
        ]