from django.test import TestCase
from main.controller.logic import RestaurantStatisticsLogic
from main.model.models import ChoicesOfTheWeek, Restaurant, Vote
from users.models import Team
from django.contrib.auth import get_user_model

User = get_user_model()


class RestaurantStatisticsLogicTest(TestCase):
    restaurantStatisticsLogic = RestaurantStatisticsLogic()

    def setUp(self):
        team = Team.objects.create(team_name="TestTeam")
        other_team = Team.objects.create(team_name="otherTeam")
        first_restaurant = Restaurant.objects.create(restaurant_name='first_restaurant', restaurant_color='#ffffff',
                                                     restaurant_for_team=team)
        second_restaurant = Restaurant.objects.create(restaurant_name='second_restaurant',
                                                      restaurant_for_team=team)
        other_restaurant = Restaurant.objects.create(restaurant_name='other_restaurant',
                                                     restaurant_for_team=other_team)

        ChoicesOfTheWeek.objects.create(restaurant=first_restaurant)
        ChoicesOfTheWeek.objects.create(restaurant=first_restaurant)
        ChoicesOfTheWeek.objects.create(restaurant=second_restaurant)
        ChoicesOfTheWeek.objects.create(restaurant=other_restaurant)

        testUser = User.objects.create(username='testUser', is_staff=True)
        testUser.set_password('12345')
        testUser.team = team
        testUser.save()
        otherUser = User.objects.create(username='otherUser', is_staff=True)
        otherUser.set_password('12345')
        otherUser.team = other_team
        otherUser.save()

        Vote.objects.create(restaurant=first_restaurant, user=testUser)
        Vote.objects.create(restaurant=other_restaurant, user=otherUser)

    def test_get_different_restaurant_names(self):
        team = self.get_test_team()
        names = self.restaurantStatisticsLogic.get_different_restaurant_names_from_team(team)
        self.assertEquals(names, {'first_restaurant', 'second_restaurant'})

    def test_get_votes_for_restaurants(self):
        team = self.get_test_team()
        restaurant = Restaurant.objects.get(restaurant_name='first_restaurant')
        votes = self.restaurantStatisticsLogic.get_votes_for_restaurant_name_from_team(restaurant.restaurant_name,
                                                                                       team)
        self.assertEquals(votes, 2)

    def test_get_choice_of_the_days_with_votes(self):
        team = self.get_test_team()
        choice = self.restaurantStatisticsLogic.get_restaurants_that_have_votes_from_team(team)
        self.assertEquals(choice, {'first_restaurant': 1})

    def test_get_color_for_restaurant_names(self):
        team = self.get_test_team()
        color = self.restaurantStatisticsLogic.get_color_for_restaurant_name_for_team('first_restaurant', team)
        self.assertEquals(color, '#ffffff')

    def get_test_team(self):
        return Team.objects.get(team_name="TestTeam")
