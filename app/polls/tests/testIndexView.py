from django.contrib.auth.models import User
from django.urls import reverse
from polls.tests import SetUpTests
from polls.persistence import Restaurant
from absenceCalendar.models import Absence
from utils.enum import Reasons


class IndexViewTest(SetUpTests):
    def test_index(self):
        offenbach = Restaurant.objects.get(restaurant_name='Offenbach')

        response = self.client.get(reverse('polls:index'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context[-1]['restaurant_list']), 4)
        self.assertEquals(response.context[-1]['choice_of_the_day'][0], offenbach)
        self.assertEquals(response.context[-1]['supporters'], ['erster_test_user', 'zweiter_test_user'])

    def test_vote(self):
        response = self.client.post('/vote/')
        self.assertRedirects(response, '/admin/login/?next=/vote/', status_code=302)

        response = self.client.post('/admin/login/?next=/vote/', {'username': 'erster_test_user', 'password': '12345'})
        self.assertRedirects(response, '/vote/', status_code=302, target_status_code=302)

        Restaurant.objects.create(restaurant_name='Super Salad')
        response = self.client.post('/vote/', {'voteButton': "Super Salad"})
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
        print(Absence.objects.all())
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
