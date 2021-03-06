import collections
import structlog
from main.model.persistence import RestaurantDAO, VoteDAO

logger = structlog.getLogger(__name__)


class RestaurantLogic:
    restaurant_dao = RestaurantDAO()
    vote_dao = VoteDAO()

    def get_all_restaurants_from_team(self, team):
        logger.debug("get all restaurants")
        return self.restaurant_dao.get_all_restaurants_from_team(team)

    def get_restaurants_with_ids(self, restaurants_ids):
        logger.debug("get restaurant with ids: %s" % restaurants_ids)
        return self.restaurant_dao.get_restaurants_with_ids(restaurants_ids)

    def get_restaurants_with_votes_from_team(self, team):
        logger.debug("get restaurants with number of votes")
        restaurant_dict = {
            restaurant: self.get_votes_for_restaurant_with_id(restaurant.id)
            for restaurant in self.get_all_restaurants_from_team(team)
        }
        return self.sort_restaurant_dict(restaurant_dict)

    def get_votes_for_restaurant_with_id(self, restaurant_id):
        logger.debug("get votes for restaurants with id: %s" % restaurant_id)
        vote_queryset = self.vote_dao.get_counted_votes(restaurant_id)
        votes = vote_queryset.filter(restaurant_id=restaurant_id)
        if votes:
            return votes.values_list('restaurant_count', flat=True).get()
        else:
            logger.debug("there is no vote for that restaurant with id: %s" % restaurant_id)
            return 0

    def get_restaurants_with_names_for_team(self, restaurant_names, team):
        logger.debug("get restaurants with names: %s" % restaurant_names)
        return [self.restaurant_dao.get_restaurant_with_name_for_team(name, team) for name in restaurant_names]

    def sort_restaurant_dict(self, restaurant_dict):
        logger.debug("sorting this restaurants dict after votes: %s" % restaurant_dict)
        sorted_restaurant_dict = sorted(restaurant_dict.items(), key=lambda kv: kv[1], reverse=True)
        return collections.OrderedDict(sorted_restaurant_dict)
