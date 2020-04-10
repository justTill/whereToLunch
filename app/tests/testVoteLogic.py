from django.contrib.auth.models import User
from polls.logic import VoteLogic
from polls.tests import SetUpTestss
from polls.models import Restaurant, Vote


class VoteLogicTest(SetUpTestss):
    voteLogic = VoteLogic()

    def test_choice_of_the_day(self):
        choice_of_the_day = self.voteLogic.choice_of_the_day()

        self.assertEquals(len(choice_of_the_day), 1)
        self.assertIn('first_restaurant', choice_of_the_day[0].__str__())

        user = User.objects.create(username='test_user', is_staff=True)
        user.set_password('12345')
        user.save()

        user2 = User.objects.create(username='test_user2', is_staff=True)
        user2.set_password('12345')
        user2.save()

        restaurant = Restaurant.objects.create(restaurant_name='restaurant')
        Vote.objects.create(restaurant=restaurant, user=user)
        Vote.objects.create(restaurant=restaurant, user=user2)

        choice_of_the_day = self.voteLogic.choice_of_the_day()
        self.assertIn('first_restaurant', choice_of_the_day[0].__str__())
        self.assertIn('restaurant', choice_of_the_day[1].__str__())

    def test_delete_votes_from_user(self):
        user = User.objects.get(username='second_test_user')
        self.voteLogic.delete_votes_from_user(user)
        self.assertEquals(list(self.voteLogic.get_votes_from_user(user)), [])
