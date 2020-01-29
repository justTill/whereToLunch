from restaurantStatistics.tests import SetUpTests
from restaurantStatistics.logic import RestaurantStatisticsLogic
from polls.models import Restaurant


class RestaurantLogicTest(SetUpTests):
    restaurantStatisticsLogic = RestaurantStatisticsLogic()

    def test_getDifferentRestaurantNames(self):
        """There are 3 Choices 2x Offenbach and 1x zucchini -> so result = 1x both"""
        names = self.restaurantStatisticsLogic.get_different_restaurant_names()
        self.assertEquals(names, {'Offenbach', 'Zucchini'})

    def test_getVotesForRestaurants(self):
        offenbach = Restaurant.objects.get(restaurant_name='Offenbach')
        votes = self.restaurantStatisticsLogic.get_votes_for_restaurant_name(offenbach.restaurant_name)
        self.assertEquals(votes, 2)

    def test_getChoiceOfTheDaysWithVotes(self):
        choice = self.restaurantStatisticsLogic.get_restaurants_that_have_votes()
        self.assertEquals(choice, {'Offenbach': 1})

    def test_getColorForRestaurantNames(self):
        color = self.restaurantStatisticsLogic.get_color_for_restaurant_name('Offenbach')
        self.assertEquals(color, '#ffffff')
