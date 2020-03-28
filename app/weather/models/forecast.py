from django.db import models
from django.utils import timezone
from utils.date import dateManager


class Forecast(models.Model):
    timestamp = models.DateTimeField()
    temperature = models.DecimalField(max_digits=12, decimal_places=2)
    weather_group = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    icon_id = models.CharField(max_length=5)

    def save(self, *args, **kwargs):
        if not self.id:
            dateManager.activate_timezone()
            self.timestamp = timezone.now()
        return super(Forecast, self).save(*args, **kwargs)

    def __str__(self):
        return self.timestamp.strftime('%d %B %Y um %H:%M ')
