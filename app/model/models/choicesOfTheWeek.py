from django.db import models
from django.utils import timezone
from polls.models import Restaurant


class ChoicesOfTheWeek(models.Model):
    timestamp = models.DateTimeField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        return super(ChoicesOfTheWeek, self).save(*args, **kwargs)

    def __str__(self):
        return 'Choice = ' + self.restaurant.__str__()
