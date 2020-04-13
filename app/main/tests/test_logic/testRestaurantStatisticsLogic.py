from django.contrib.auth.models import User
from django.test import TestCase
from main.controller.logic import RestaurantStatisticsLogic
from main.model.models import ChoicesOfTheWeek, Restaurant, Vote


class RestaurantLogicTest(TestCase):
    restaurantStatisticsLogic = RestaurantStatisticsLogic()

    def setUp(self):
        first_restaurant = Restaurant.objects.create(restaurant_name='first_restaurant', restaurant_color='#ffffff')
        second_restaurant = Restaurant.objects.create(restaurant_name='second_restaurant')

        ChoicesOfTheWeek.objects.create(restaurant=first_restaurant)
        ChoicesOfTheWeek.objects.create(restaurant=first_restaurant)
        ChoicesOfTheWeek.objects.create(restaurant=second_restaurant)

        testUser = User.objects.create(username='testUser', is_staff=True)
        testUser.set_password('12345')
        testUser.save()

        Vote.objects.create(restaurant=first_restaurant, user=testUser)

    def test_get_different_restaurant_names(self):
        names = self.restaurantStatisticsLogic.get_different_restaurant_names()
        self.assertEquals(names, {'first_restaurant', 'second_restaurant'})

    def test_get_votes_for_restaurants(self):
        restaurant = Restaurant.objects.get(restaurant_name='first_restaurant')
        votes = self.restaurantStatisticsLogic.get_votes_for_restaurant_name(restaurant.restaurant_name)
        self.assertEquals(votes, 2)

    def test_get_choice_of_the_days_with_votes(self):
        choice = self.restaurantStatisticsLogic.get_restaurants_that_have_votes()
        self.assertEquals(choice, {'first_restaurant': 1})

    def test_get_color_for_restaurant_names(self):
        color = self.restaurantStatisticsLogic.get_color_for_restaurant_name('first_restaurant')
        self.assertEquals(color, '#ffffff')
