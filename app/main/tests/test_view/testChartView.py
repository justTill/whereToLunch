from django.test import TestCase
from django.urls import reverse
from main.model.models import ChoicesOfTheWeek, Restaurant, Vote
from users.models import Team
from django.contrib.auth import get_user_model

User = get_user_model()


class ChartView(TestCase):
    def setUp(self):
        team = Team.objects.create(team_name="testTeam")
        first_restaurant = Restaurant.objects.create(restaurant_name='first_restaurant', restaurant_color='#ffffff',
                                                     restaurant_for_team=team)
        second_restaurant = Restaurant.objects.create(restaurant_name='second_restaurant', restaurant_for_team=team)

        testUser = User.objects.create(username='testUser', is_staff=True)
        testUser.set_password('12345')
        testUser.slack_member_id = "member_id"
        testUser.user_image = "image_url"
        testUser.team = team
        testUser.save()

        ChoicesOfTheWeek.objects.create(restaurant=first_restaurant)
        ChoicesOfTheWeek.objects.create(restaurant=first_restaurant)
        ChoicesOfTheWeek.objects.create(restaurant=second_restaurant)

        Vote.objects.create(restaurant=first_restaurant, user=testUser)

    def test_VotesChart(self):
        self.client.post('/admin/login/?next=/vote/', {'username': 'testUser', 'password': '12345'})
        response = self.client.get(reverse('main:api-charts-votes'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data['restaurants_with_votes'],
                          [{'name': 'first_restaurant', 'supporters': [' testUser'], 'color': '#ffffff',
                            'images': ['/mediafiles/image_url']}])

    def test_ChoicesChart(self):
        self.client.post('/admin/login/?next=/vote/', {'username': 'testUser', 'password': '12345'})
        response = self.client.get(reverse('main:api-charts-choices'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1)
        self.assertIn({'name': 'second_restaurant', 'times_won': 1, 'color': '#ffffff'},
                      response.data['choices_of_the_past'])
        self.assertIn({'name': 'first_restaurant', 'times_won': 2, 'color': '#ffffff'},
                      response.data['choices_of_the_past'])
