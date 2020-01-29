import collections
from polls.persistence import RestaurantDAO, VoteDAO


class RestaurantLogic:
    restaurant_dao = RestaurantDAO()
    vote_dao = VoteDAO()

    def get_all_restaurants(self):
        return self.restaurant_dao.get_all_restaurants()

    def get_restaurants_with_ids(self, restaurants_ids):
        return self.restaurant_dao.get_restaurants_with_ids(restaurants_ids)

    def get_restaurants_with_votes(self):
        restaurant_dict = {
            restaurant: self.get_votes_for_restaurant_with_id(restaurant.id)
            for restaurant in self.get_all_restaurants()
        }
        return self.sort_restaurant_dict(restaurant_dict)

    def get_votes_for_restaurant_with_id(self, restaurant_id):
        vote_queryset = self.vote_dao.get_counted_votes()
        votes = vote_queryset.filter(restaurant_id=restaurant_id)
        if votes:
            return votes.values_list('restaurant_count', flat=True).get()
        else:
            return 0

    def get_restaurants_with_names(self, restaurant_names):
        return [self.restaurant_dao.get_restaurant_with_name(name) for name in restaurant_names]

    def sort_restaurant_dict(self, restaurant_dict):
        sorted_restaurant_dict = sorted(restaurant_dict.items(), key=lambda kv: kv[1], reverse=True)
        return collections.OrderedDict(sorted_restaurant_dict)
