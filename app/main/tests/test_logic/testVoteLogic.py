from django.contrib.auth.models import User
from django.test import TestCase
from main.controller.logic import VoteLogic
from main.model.models import Restaurant, Vote


class VoteLogicTest(TestCase):
    voteLogic = VoteLogic()

    def setUp(self):
        first_restaurant = Restaurant.objects.create(restaurant_name='first_restaurant')
        second_restaurant = Restaurant.objects.create(restaurant_name='second_restaurant')

        first_test_user = User.objects.create(username='first_test_user', is_staff=True)
        first_test_user.set_password('12345')
        first_test_user.save()
        Vote.objects.create(restaurant=first_restaurant, user=first_test_user)

        second_test_user = User.objects.create(username='second_test_user', is_staff=True)
        second_test_user.set_password('12345')
        second_test_user.save()

    def test_choice_of_the_day(self):
        choice_of_the_day = self.voteLogic.choice_of_the_day()
        self.assertEquals(len(choice_of_the_day), 1)
        self.assertIn('first_restaurant', choice_of_the_day[0].__str__())

        user = User.objects.create(username='test_user', is_staff=True)
        user.set_password('12345')
        user.save()

        restaurant = Restaurant.objects.create(restaurant_name='restaurant')
        Vote.objects.create(restaurant=restaurant, user=user)

        choice_of_the_day = self.voteLogic.choice_of_the_day()
        self.assertIn('first_restaurant', choice_of_the_day[0].__str__())
        self.assertIn('restaurant', choice_of_the_day[1].__str__())

    def test_delete_votes_from_user(self):
        user = User.objects.get(username='second_test_user')
        self.voteLogic.delete_votes_from_user(user)
        self.assertEquals(list(self.voteLogic.get_votes_from_user(user)), [])
