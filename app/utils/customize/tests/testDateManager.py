import datetime
from django.utils import timezone
from unittest import TestCase
from utils.date import dateManager


class TestDateManager(TestCase):

    def test_today(self):
        self.assertEqual(dateManager.today(), datetime.date.today())

    def test_tomorrow(self):
        self.assertEqual(dateManager.tomorrow(), datetime.date.today() + datetime.timedelta(days=1))

    def test_is_after_noon(self):
        now = timezone.now() + datetime.timedelta(hours=1)
        now = now.time().strftime('%H:%M')
        noon = timezone.now().time().replace(hour=12, minute=30, second=0).strftime('%H:%M')

        if now >= noon:
            self.assertEqual(dateManager.current_vote_day(), datetime.date.today() + datetime.timedelta(days=1))
        else:
            self.assertEqual(dateManager.current_vote_day(), datetime.date.today())

