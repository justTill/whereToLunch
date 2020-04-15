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

    def get_different_restaurant_names_from_team(self, team):
        logger.debug("get different restaurants names that won at least one time")
        choices = self.restaurant_statistics_dao.get_restaurant_names_from_team(team)
        restaurant_dict = {c.restaurant.restaurant_name for c in choices}
        return restaurant_dict

    def get_votes_for_restaurant_name(self, restaurant_name):
        logger.debug("get current votes for a restaurant with the name %s " % restaurant_name)
        vote = self.restaurant_statistics_dao.get_votes_for_restaurant(
            self.restaurant_dao.get_restaurant_with_name_for_team(restaurant_name)
        )
        return vote

    def get_restaurants_that_have_votes_from_team(self, team):
        logger.debug("get all restaurants that have at least one vote")
        return {
                restaurant.restaurant_name: vote
                for restaurant, vote
                in self.restaurant_logic.get_restaurants_with_votes_from_team(team).items()
                if vote != 0
            }

    def get_color_for_restaurant_name_for_team(self, restaurant_name, team):
        return self.restaurant_dao.get_color_for_restaurant_with_name_for_team(restaurant_name, team)

    def get_current_vote_statistics_data_for_team(self, team):
        logger.debug("process current vote statistics data, and get them in order for json endpoint")
        restaurants_that_have_votes = self.get_restaurants_that_have_votes_from_team(team)
        data = []
        for restaurant in restaurants_that_have_votes:
            data.append({
                'name': restaurant,
                'supporters': [' ' + user_name.get('user__username')
                               for user_name in self.vote_logic.get_votes_for_restaurant_with_name_for_team(restaurant, team)],
                'color': self.get_color_for_restaurant_name_for_team(restaurant, team),
                'images': [self.get_image_from_user(user)
                           for user in self.vote_logic.get_votes_for_restaurant_with_name_for_team(restaurant, team)]
            })
        return data

    def get_choices_of_the_past_from_team(self, team):
        logger.debug("process restaurant data of the past and collect information for the json endpoint ")
        restaurant_names = self.get_different_restaurant_names_from_team(team)
        data = []
        for name in restaurant_names:
            data.append({
                'name': name,
                'times_won': self.get_votes_for_restaurant_name(name),
                'color': self.get_color_for_restaurant_name_for_team(name, team)
            })
        return data

    def get_image_from_user(self, user):
        return self.user_logic.get_image_from_user(user)
