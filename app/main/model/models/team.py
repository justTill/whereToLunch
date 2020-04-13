from django.db import models


class Team(models.Model):
    team_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.team_name
