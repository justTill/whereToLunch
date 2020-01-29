from django.contrib.auth.models import User
from django.db import models
from .restaurant import Restaurant


class Vote(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Restaurant=" + self.restaurant.__str__() + "/Name=" + self.user.username
