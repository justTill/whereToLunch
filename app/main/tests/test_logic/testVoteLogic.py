from django.test import TestCase
from main.controller.logic import VoteLogic
from main.model.models import Restaurant, Vote
from users.models import Team
from django.contrib.auth import get_user_model

User = get_user_model()


class VoteLogicTest(TestCase):
    voteLogic = VoteLogic()

    def setUp(self):
        team = Team.objects.create(team_name="testTeam")
        first_restaurant = Restaurant.objects.create(restaurant_name='first_restaurant', restaurant_for_team=team)

        first_test_user = User.objects.create(username='first_test_user', is_staff=True)
        first_test_user.set_password('12345')
        first_test_user.team = team
        first_test_user.save()
        Vote.objects.create(restaurant=first_restaurant, user=first_test_user)

        second_test_user = User.objects.create(username='second_test_user', is_staff=True)
        second_test_user.set_password('12345')
        second_test_user.team = team
        second_test_user.save()

    def test_choice_of_the_day(self):
        team = Team.objects.get(team_name="testTeam")
        choice_of_the_day = self.voteLogic.choice_of_the_day_for_team(team)
        self.assertEquals(len(choice_of_the_day), 1)
        self.assertIn('first_restaurant', choice_of_the_day[0].__str__())

        user = User.objects.create(username='test_user', is_staff=True)
        user.set_password('12345')
        user.team = team
        user.save()

        restaurant = Restaurant.objects.create(restaurant_name='restaurant', restaurant_for_team=team)
        Vote.objects.create(restaurant=restaurant, user=user)

        choice_of_the_day = self.voteLogic.choice_of_the_day_for_team(team)
        self.assertIn('first_restaurant', choice_of_the_day[0].__str__())
        self.assertIn('restaurant', choice_of_the_day[1].__str__())

    def test_delete_votes_from_user(self):
        user = User.objects.get(username='second_test_user')
        self.voteLogic.delete_votes_from_user(user)
        self.assertEquals(list(self.voteLogic.get_votes_from_user(user)), [])
