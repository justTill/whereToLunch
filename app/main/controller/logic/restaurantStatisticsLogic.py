import structlog
from main.model.persistence import RestaurantDAO, RestaurantStatisticsDAO
from .voteLogic import VoteLogic
from .resturantLogic import RestaurantLogic
from .userLogic import UserLogic

logger = structlog.getLogger(__name__)


class RestaurantStatisticsLogic:
    restaurant_statistics_dao = RestaurantStatisticsDAO()
    restaurant_dao = RestaurantDAO()
    restaurant_logic = RestaurantLogic()
    vote_logic = VoteLogic()
    user_logic = UserLogic()

    def get_different_restaurant_names(self):
        logger.debug("get different restaurants names that one at least on time")
        choices = self.restaurant_statistics_dao.get_restaurant_names()
        restaurant_dict = {c.restaurant.restaurant_name for c in choices}
        return restaurant_dict

    def get_votes_for_restaurant_name(self, restaurant_name):
        logger.debug("get current votes for a restaurant with the name %s " % restaurant_name)
        vote = self.restaurant_statistics_dao.get_votes_for_restaurant(
            self.restaurant_dao.get_restaurant_with_name(restaurant_name)
        )
        return vote

    def get_restaurants_that_have_votes(self):
        logger.debug("get all restaurants that have at least one vote")
        return {
                restaurant.restaurant_name: vote
                for restaurant, vote
                in self.restaurant_logic.get_restaurants_with_votes_from_team().items()
                if vote != 0
            }

    def get_color_for_restaurant_name(self, restaurant_name):
        return self.restaurant_dao.get_color_for_restaurant_with_name(restaurant_name)

    def get_current_vote_statistics_data(self):
        logger.debug("process current vote statistics data, and get them in order for json endpoint")
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
        logger.debug("process restaurant data of the past and collect information for the json endpoint ")
        restaurant_names = self.get_different_restaurant_names()
        data = []
        for name in restaurant_names:
            data.append({
                'name': name,
                'times_won': self.get_votes_for_restaurant_name(name),
                'color': self.get_color_for_restaurant_name(name)
            })
        return data

    def get_image_from_user(self, user):
        return self.user_logic.get_image_from_user(user)
