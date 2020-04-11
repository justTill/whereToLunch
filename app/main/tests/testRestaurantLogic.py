from main.tests.testSetUpP import SetUpTestss
from main.controller.logic import RestaurantLogic
from main.model.models import Restaurant


class RestaurantLogicTest(SetUpTestss):

    def test_restaurantsWithVotes(self):
        restaurantLogic = RestaurantLogic()
        restaurantSet = restaurantLogic.get_restaurants_with_votes()
        first_restaurant = Restaurant.objects.get(restaurant_name='first_restaurant')
        second_restaurant = Restaurant.objects.get(restaurant_name='second_restaurant')
        third_restaurant = Restaurant.objects.get(restaurant_name='third_restaurant')
        fourth_restaurant = Restaurant.objects.get(restaurant_name='fourth_restaurant')

        self.assertEquals(len(restaurantSet), 4)

        self.assertIn(first_restaurant, restaurantSet)

        # #Check if they have the right Amounts
        self.assertEquals(restaurantSet.get(first_restaurant), 2)
        self.assertEquals(restaurantSet.get(second_restaurant), 1)
        self.assertEquals(restaurantSet.get(third_restaurant), 1)
        self.assertEquals(restaurantSet.get(fourth_restaurant), 0)

        # Check if they are Sorted after Votes
        # second Criteria are Names
        self.assertEquals(restaurantSet.items(), {(first_restaurant, 2), (third_restaurant, 1), (second_restaurant, 1), (fourth_restaurant, 0)})
