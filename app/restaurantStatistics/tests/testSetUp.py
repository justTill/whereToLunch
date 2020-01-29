from django.contrib.auth.models import User
from django.test import TestCase
from polls.models import Restaurant, Vote
from restaurantStatistics.models import ChoicesOfTheWeek


class SetUpTests(TestCase):
    def setUp(self):
        offenbach = Restaurant.objects.create(restaurant_name='Offenbach', restaurant_color='#ffffff')
        zucchini = Restaurant.objects.create(restaurant_name='Zucchini')
        ChoicesOfTheWeek.objects.create(restaurant=offenbach)
        ChoicesOfTheWeek.objects.create(restaurant=offenbach)
        ChoicesOfTheWeek.objects.create(restaurant=zucchini)

        testUser = User.objects.create(username='testUser', is_staff=True)
        testUser.set_password('12345')
        testUser.save()
        Vote.objects.create(restaurant=offenbach, user=testUser)
