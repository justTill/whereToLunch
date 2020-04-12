from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from main.model.models import ChoicesOfTheWeek, Restaurant, Vote, Profile


class ChartView(TestCase):
    def setUp(self):
        first_restaurant = Restaurant.objects.create(restaurant_name='first_restaurant', restaurant_color='#ffffff')
        second_restaurant = Restaurant.objects.create(restaurant_name='second_restaurant')

        testUser = User.objects.create(username='testUser', is_staff=True)
        testUser.set_password('12345')
        testUser.save()

        ChoicesOfTheWeek.objects.create(restaurant=first_restaurant)
        ChoicesOfTheWeek.objects.create(restaurant=first_restaurant)
        ChoicesOfTheWeek.objects.create(restaurant=second_restaurant)

        profile = Profile.objects.get(user=testUser)
        profile.slack_member_id = "member_id"
        profile.userImage = "image_url"
        profile.save()

        Vote.objects.create(restaurant=first_restaurant, user=testUser)

    def test_VotesChart(self):
        response = self.client.get(reverse('main:api-charts-votes'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data['restaurants_with_votes'],
                          [{'name': 'first_restaurant', 'supporters': [' testUser'], 'color': '#ffffff', 'images': ['/mediafiles/image_url']}])

    def test_ChoicesChart(self):
        response = self.client.get(reverse('main:api-charts-choices'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1)
        print(response.data)
        self.assertIn({'name': 'second_restaurant', 'times_won': 1, 'color': '#ffffff'}, response.data['choices_of_the_past'])
        self.assertIn({'name': 'first_restaurant', 'times_won': 2, 'color': '#ffffff'}, response.data['choices_of_the_past'])
