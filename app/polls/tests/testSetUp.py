import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from polls.models import Restaurant, Vote
from weather.models import Forecast
from absenceCalendar.models import Absence
from utils.enum import Reasons


class SetUpTests(TestCase):
    today = datetime.date.today()

    def setUp(self):
        offenbach = Restaurant.objects.create(restaurant_name='Offenbach')
        zucchini = Restaurant.objects.create(restaurant_name='Zucchini')
        stinkeburger = Restaurant.objects.create(restaurant_name='Stinkeburger')
        Restaurant.objects.create(restaurant_name='Purino')

        erster_test_user = User.objects.create(username='erster_test_user', is_staff=True)
        erster_test_user.set_password('12345')
        erster_test_user.save()

        zweiter_test_user = User.objects.create(username='zweiter_test_user', is_staff=True)
        zweiter_test_user.set_password('12345')
        zweiter_test_user.save()

        dritter_test_user = User.objects.create(username='dritter_test_user', is_staff=True)
        dritter_test_user.set_password('12345')
        dritter_test_user.save()

        vierter_test_user = User.objects.create(username='vierter_test_user', is_staff=True)
        vierter_test_user.set_password('12345')
        vierter_test_user.save()

        Vote.objects.create(restaurant=offenbach, user=erster_test_user)
        Vote.objects.create(restaurant=offenbach, user=zweiter_test_user)
        Vote.objects.create(restaurant=stinkeburger, user=dritter_test_user)
        Vote.objects.create(restaurant=zucchini, user=vierter_test_user)

        Forecast.objects.create(temperature=12, description="sunny")

        Absence.objects.create(user=erster_test_user,
                               absenceFrom=self.today,
                               absenceTo=self.today,
                               reason=Reasons.ABSENT.value
                               )
        Absence.objects.create(user=erster_test_user,
                               absenceFrom=self.today + datetime.timedelta(days=1),
                               absenceTo=self.today + datetime.timedelta(days=1),
                               reason=Reasons.ABSENT.value
                               )

        Absence.objects.create(user=zweiter_test_user,
                               absenceFrom=self.today,
                               absenceTo=self.today,
                               reason=Reasons.DONOTCARE.value
                               )
        Absence.objects.create(user=vierter_test_user,
                               absenceFrom=self.today,
                               absenceTo=self.today,
                               reason=Reasons.OUT.value
                               )