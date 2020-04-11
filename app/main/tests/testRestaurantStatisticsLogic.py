from main.tests.testSetUp import SetUpTests
from main.controller.logic import RestaurantStatisticsLogic
from main.model.models import Restaurant


class RestaurantLogicTest(SetUpTests):
    restaurantStatisticsLogic = RestaurantStatisticsLogic()

    def test_get_different_restaurant_names(self):
        """There are 3 Choices 2x Offenbach and 1x zucchini -> so result = 1x both"""
        names = self.restaurantStatisticsLogic.get_different_restaurant_names()
        self.assertEquals(names, {'Offenbach', 'Zucchini'})

    def test_get_votes_for_restaurants(self):
        offenbach = Restaurant.objects.get(restaurant_name='Offenbach')
        votes = self.restaurantStatisticsLogic.get_votes_for_restaurant_name(offenbach.restaurant_name)
        self.assertEquals(votes, 2)

    def test_get_choice_of_the_days_with_votes(self):
        choice = self.restaurantStatisticsLogic.get_restaurants_that_have_votes()
        self.assertEquals(choice, {'Offenbach': 1})

    def test_get_color_for_restaurant_names(self):
        color = self.restaurantStatisticsLogic.get_color_for_restaurant_name('Offenbach')
        self.assertEquals(color, '#ffffff')
