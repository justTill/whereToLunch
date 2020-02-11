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
        burger = Restaurant.objects.create(restaurant_name='burger')
        Restaurant.objects.create(restaurant_name='Purino')

        first_test_user = User.objects.create(username='first_test_user', is_staff=True)
        first_test_user.set_password('12345')
        first_test_user.save()

        second_test_user = User.objects.create(username='second_test_user', is_staff=True)
        second_test_user.set_password('12345')
        second_test_user.save()

        third_test_user = User.objects.create(username='third_test_user', is_staff=True)
        third_test_user.set_password('12345')
        third_test_user.save()

        fourth_test_user = User.objects.create(username='fourth_test_user', is_staff=True)
        fourth_test_user.set_password('12345')
        fourth_test_user.save()

        Vote.objects.create(restaurant=offenbach, user=first_test_user)
        Vote.objects.create(restaurant=offenbach, user=second_test_user)
        Vote.objects.create(restaurant=burger, user=third_test_user)
        Vote.objects.create(restaurant=zucchini, user=fourth_test_user)

        Forecast.objects.create(temperature=12, description="sunny")

        Absence.objects.create(user=first_test_user,
                               absenceFrom=self.today,
                               absenceTo=self.today,
                               reason=Reasons.ABSENT.value
                               )
        Absence.objects.create(user=first_test_user,
                               absenceFrom=self.today + datetime.timedelta(days=1),
                               absenceTo=self.today + datetime.timedelta(days=1),
                               reason=Reasons.ABSENT.value
                               )

        Absence.objects.create(user=second_test_user,
                               absenceFrom=self.today,
                               absenceTo=self.today,
                               reason=Reasons.DONOTCARE.value
                               )
        Absence.objects.create(user=fourth_test_user,
                               absenceFrom=self.today,
                               absenceTo=self.today,
                               reason=Reasons.OUT.value
                               )