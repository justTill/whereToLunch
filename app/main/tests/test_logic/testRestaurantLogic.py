from django.test import TestCase
from main.controller.logic import RestaurantLogic
from main.model.models import Restaurant, Vote
from users.models import Team
from django.contrib.auth import get_user_model

User = get_user_model()


class RestaurantLogicTest(TestCase):

    def setUp(self):
        team = Team.objects.create(team_name="testTeam")
        other_team = Team.objects.create(team_name="other_team")
        first_restaurant = Restaurant.objects.create(restaurant_name='first_restaurant', restaurant_for_team=team)
        second_restaurant = Restaurant.objects.create(restaurant_name='second_restaurant', restaurant_for_team=team)
        third_restaurant = Restaurant.objects.create(restaurant_name='third_restaurant', restaurant_for_team=team)
        Restaurant.objects.create(restaurant_name='fourth_restaurant', restaurant_for_team=team)
        other_restaurant = Restaurant.objects.create(restaurant_name='other_restaurant', restaurant_for_team=other_team)

        first_test_user = User.objects.create(username='first_test_user', is_staff=True)
        first_test_user.set_password('12345')
        first_test_user.team = team
        first_test_user.save()
        other_test_user = User.objects.create(username='other_test_user', is_staff=True)
        other_test_user.set_password('12345')
        other_test_user.team = other_team
        other_test_user.save()

        Vote.objects.create(restaurant=first_restaurant, user=first_test_user)
        Vote.objects.create(restaurant=first_restaurant, user=first_test_user)
        Vote.objects.create(restaurant=third_restaurant, user=first_test_user)
        Vote.objects.create(restaurant=second_restaurant, user=first_test_user)
        Vote.objects.create(restaurant=other_restaurant, user=other_test_user)

    def test_restaurantsWithVotes(self):
        team = Team.objects.get(team_name="testTeam")
        restaurantLogic = RestaurantLogic()
        restaurantSet = restaurantLogic.get_restaurants_with_votes_from_team(team)
        first_restaurant = Restaurant.objects.get(restaurant_name='first_restaurant')
        second_restaurant = Restaurant.objects.get(restaurant_name='second_restaurant')
        third_restaurant = Restaurant.objects.get(restaurant_name='third_restaurant')
        fourth_restaurant = Restaurant.objects.get(restaurant_name='fourth_restaurant')

        self.assertEquals(len(restaurantSet), 4)

        self.assertIn(first_restaurant, restaurantSet)

        # #Check if they have the right Amounts
        self.assertEquals(restaurantSet.get(first_restaurant), 2)
        self.assertEquals(restaurantSet.get(second_restaurant), 1)
        self.assertEquals(restaurantSet.get(third_restaurant), 1)
        self.assertEquals(restaurantSet.get(fourth_restaurant), 0)

        # Check if they are Sorted after Votes
        # second Criteria are Names
        self.assertEquals(restaurantSet.items(),
                          {(first_restaurant, 2), (third_restaurant, 1), (second_restaurant, 1),
                           (fourth_restaurant, 0)})
