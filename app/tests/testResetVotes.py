import datetime
from unittest import TestCase
from polls.models import Restaurant, Vote
from absenceCalendar.models import Absence
from utils.enum import Reasons
from utils.date import dateManager
from django.contrib.auth.models import User
from utils import resetVotes
from restaurantStatistics.models import ChoicesOfTheWeek


class TestResetVotes(TestCase):
    yesterday = dateManager.today() + datetime.timedelta(days=-1)

    def test_reset_things_from_last_vote_day(self):
        User.objects.all().delete()
        Restaurant.objects.all().delete()
        Vote.objects.all().delete()
        Absence.objects.all().delete()

        first = User.objects.create(username="first")
        second = User.objects.create(username="second")
        restaurant = Restaurant.objects.create(restaurant_name="test_restaurant")
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
