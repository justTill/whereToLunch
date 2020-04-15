import datetime
from unittest import TestCase
from main.model.models import Absence, Vote, Restaurant, ChoicesOfTheWeek
from utils.enum import Reasons
from utils.date import dateManager
from utils import resetVotes
from users.models import Team
from django.contrib.auth import get_user_model

User = get_user_model()


class TestResetVotes(TestCase):
    yesterday = dateManager.today() + datetime.timedelta(days=-1)

    def test_reset_things_from_last_vote_day(self):
        team = Team.objects.create(team_name="testTeam")
        other_team = Team.objects.create(team_name="otherTeam")
        User.objects.all().delete()
        Restaurant.objects.all().delete()
        Vote.objects.all().delete()
        Absence.objects.all().delete()

        first = User.objects.create(username="first", team=team)
        second = User.objects.create(username="second", team=other_team)
        restaurant = Restaurant.objects.create(restaurant_name="test_restaurant", restaurant_for_team=other_team)
        Absence.objects.create(user=first,
                               absenceFrom=self.yesterday,
                               absenceTo=self.yesterday,
                               reason=Reasons.OUT.value)
        Vote.objects.create(restaurant=restaurant, user=second)

        self.assertEqual(len(User.objects.all()), 2)
        self.assertEqual(Restaurant.objects.exists(), True)
        self.assertEqual(Absence.objects.exists(), True)
        self.assertEqual(Vote.objects.exists(), True)
        self.assertEqual(ChoicesOfTheWeek.objects.exists(), False)

        resetVotes.reset_things_from_last_vote_day()

        self.assertEqual(Absence.objects.exists(), False)
        self.assertEqual(Vote.objects.exists(), False)
        self.assertEqual(ChoicesOfTheWeek.objects.exists(), True)
