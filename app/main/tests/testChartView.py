from django.urls import reverse
from restaurantStatistics.tests import SetUpTests


class ChartView(SetUpTests):
    def test_VotesChart(self):
        response = self.client.get(reverse('restaurantStatistics:api-charts-votes'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data['restaurants_with_votes'],
                          [{'name': 'Offenbach', 'supporters': [' testUser'], 'color': '#ffffff', 'images': ['/mediafiles/image_url']}])

    def test_ChoicesChart(self):
        response = self.client.get(reverse('restaurantStatistics:api-charts-choices'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1)
        self.assertIn({'name': 'Zucchini', 'times_won': 1, 'color': '#ffffff'}, response.data['choices_of_the_past'])
        self.assertIn({'name': 'Offenbach', 'times_won': 2, 'color': '#ffffff'}, response.data['choices_of_the_past'])
