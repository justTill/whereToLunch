from django.test import TestCase
from django.urls import reverse
from main.model.models import Restaurant, Vote, Forecast, Absence
from utils.enum import Reasons
from users.models import Team
from django.contrib.auth import get_user_model

User = get_user_model()


class IndexViewTest(TestCase):

    def setUp(self):
        team = Team.objects.create(team_name="testTeam")
        first_restaurant = Restaurant.objects.create(restaurant_name='first_restaurant', restaurant_for_team=team)
        Restaurant.objects.create(restaurant_name='second_restaurant', restaurant_for_team=team)

        first_test_user = User.objects.create(username='first_test_user', is_staff=True)
        first_test_user.set_password('12345')
        first_test_user.team = team
        first_test_user.save()
        second_test_user = User.objects.create(username='second_test_user', is_staff=True)
        second_test_user.set_password('12345')
        second_test_user.team = team
        second_test_user.save()

        Vote.objects.create(restaurant=first_restaurant, user=first_test_user)
        Vote.objects.create(restaurant=first_restaurant, user=second_test_user)

    def test_index(self):
        first_restaurant = Restaurant.objects.get(restaurant_name='first_restaurant')
        self.client.post('/admin/login/?next=/vote/', {'username': 'first_test_user', 'password': '12345'})
        response = self.client.get(reverse('main:index'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context[-1]['restaurant_list']), 2)
        self.assertEquals(response.context[-1]['choice_of_the_day'][0], first_restaurant)
        self.assertEquals(response.context[-1]['supporters'], ['first_test_user', 'second_test_user'])

    def test_vote(self):
        response = self.client.post('/vote/')
        self.assertRedirects(response, '/admin/login/?next=/vote/', status_code=302)

        response = self.client.post('/admin/login/?next=/vote/', {'username': 'first_test_user', 'password': '12345'})
        self.assertRedirects(response, '/vote/', status_code=302, target_status_code=302)

        response = self.client.post('/vote/', {'voteButton': "first_restaurant"})
        self.assertRedirects(response, '/', status_code=302)

        self.client.post('/admin/logout')
        self.i_am_out()
        self.client.post('/admin/logout')
        self.do_not_care()

    def i_am_out(self):
        user = User.objects.create(username="out_user", is_staff=True)
        user.set_password("1234")
        user.save()
        self.client.post('/admin/login/?next=/vote/', {'username': 'out_user', 'password': '1234'})
        response = self.client.post('/iAmOut/')
        self.assertRedirects(response, '/', status_code=302)
        absence = Absence.objects.get(user=user)
        self.assertEquals(absence.reason, Reasons.OUT.value)

    def do_not_care(self):
        user = User.objects.create(username="do_not_care_user", is_staff=True)
        user.set_password("1234")
        user.save()
        self.client.post('/admin/login/?next=/vote/', {'username': 'do_not_care_user', 'password': '1234'})
        response = self.client.post('/doNotCare/')
        self.assertRedirects(response, '/', status_code=302)
        absence = Absence.objects.get(user=user)
        self.assertEquals(absence.reason, Reasons.DONOTCARE.value)
