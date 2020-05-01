import datetime
from django.contrib.auth import get_user_model
from django.db import models
from utils.enum import Reasons


class Absence(models.Model):
    ABSENCE_CHOICES = [
        (Reasons.ABSENT.value, 'absent'),
        (Reasons.OUT.value, 'do not care'),
        (Reasons.DONOTCARE.value, 'i am out'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    absenceFrom = models.DateField(default=datetime.date.today)
    absenceTo = models.DateField(default=datetime.date.today)
    reason = models.CharField(choices=ABSENCE_CHOICES, default=ABSENCE_CHOICES, max_length=20)

    def __str__(self):
        return self.user.__str__() + " von " + self.absenceFrom.__str__() + " bis " + self.absenceTo.__str__()
