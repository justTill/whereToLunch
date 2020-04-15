from django.db import models
from django.contrib.auth.models import AbstractUser


class Team(models.Model):
    team_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.team_name


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    slack_member_id = models.CharField(max_length=100, blank=True)
    user_image = models.ImageField(upload_to='images/', blank=True)
