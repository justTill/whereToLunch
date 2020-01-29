from django.urls import reverse
from polls.tests import SetUpTests
from polls.persistence import Restaurant


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

        self.delete_vote(self.client)

    def delete_vote(self, client):
        response = client.post('/iAmOut/')
        self.assertRedirects(response, '/', status_code=302)
