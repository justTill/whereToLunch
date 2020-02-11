from polls.tests import SetUpTests
from polls.logic import RestaurantLogic
from polls.models import Restaurant


class RestaurantLogicTest(SetUpTests):

    def test_restaurantsWithVotes(self):
        restaurantLogic = RestaurantLogic()
        restaurantSet = restaurantLogic.get_restaurants_with_votes()
        offenbach = Restaurant.objects.get(restaurant_name='Offenbach')
        zucchini = Restaurant.objects.get(restaurant_name='Zucchini')
        burger = Restaurant.objects.get(restaurant_name='burger')
        purino = Restaurant.objects.get(restaurant_name='Purino')

        self.assertEquals(len(restaurantSet), 4)

        self.assertIn(offenbach, restaurantSet)

        # #Check if they have the right Amounts
        self.assertEquals(restaurantSet.get(offenbach), 2)
        self.assertEquals(restaurantSet.get(zucchini), 1)
        self.assertEquals(restaurantSet.get(burger), 1)
        self.assertEquals(restaurantSet.get(purino), 0)

        # Check if they are Sorted after Votes
        # second Criteria are Names
        self.assertEquals(restaurantSet.items(), {(offenbach, 2), (burger, 1), (zucchini, 1), (purino, 0)})
