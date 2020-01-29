from restaurantStatistics.persistence import RestaurantStatisticsDAO
from polls.persistence import RestaurantDAO
from polls.logic import VoteLogic, RestaurantLogic, UserLogic


class RestaurantStatisticsLogic:
    restaurant_statistics_dao = RestaurantStatisticsDAO()
    restaurant_dao = RestaurantDAO()
    restaurant_logic = RestaurantLogic()
    vote_logic = VoteLogic()
    user_logic = UserLogic()

    def get_different_restaurant_names(self):
        choices = self.restaurant_statistics_dao.get_restaurant_names()
        restaurant_dict = {c.restaurant.restaurant_name for c in choices}
        return restaurant_dict

    def get_votes_for_restaurant_name(self, restaurant_name):
        vote = self.restaurant_statistics_dao.get_votes_for_restaurant(
            self.restaurant_dao.get_restaurant_with_name(restaurant_name)
        )

        return vote

    def get_restaurants_that_have_votes(self):
        return {
            restaurant.restaurant_name: vote
            for restaurant, vote
            in self.restaurant_logic.get_restaurants_with_votes().items()
            if vote != 0
        }

    def get_color_for_restaurant_name(self, restaurant_name):
        return self.restaurant_dao.get_color_for_restaurant_with_name(restaurant_name)

    def get_current_vote_statistics_data(self):
        restaurants_that_have_votes = self.get_restaurants_that_have_votes()
        data = []
        for restaurant in restaurants_that_have_votes:
            data.append({
                'name': restaurant,
                'supporters': [' ' + user_name.get('user__username')
                               for user_name in self.vote_logic.get_votes_for_restaurant_with_name(restaurant)],
                'color': self.get_color_for_restaurant_name(restaurant),
                'images': [self.get_image_from_user(user)
                           for user in self.vote_logic.get_votes_for_restaurant_with_name(restaurant)]
            })
        return data

    def get_choices_of_the_past(self):
        restaurant_names = self.get_different_restaurant_names()
        data = []
        for name in restaurant_names:
            data.append({
                'name': name,
                'votes': self.get_votes_for_restaurant_name(name),
                'color': self.get_color_for_restaurant_name(name)
            })
        return data

    def get_image_from_user(self, user):
        return self.user_logic.get_image_from_user(user)
