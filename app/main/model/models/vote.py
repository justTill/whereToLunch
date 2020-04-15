from django.contrib.auth import get_user_model
from django.db import models
from .restaurant import Restaurant


class Vote(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return "Restaurant=" + self.restaurant.__str__() + "/Name=" + self.user.username
