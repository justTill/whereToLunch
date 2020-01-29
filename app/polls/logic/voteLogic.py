from django.db.models import Count, Max
from polls.persistence import VoteDAO
from polls.logic import RestaurantLogic


class VoteLogic:
    vote_dao = VoteDAO()
    restaurant_logic = RestaurantLogic()

    def get_votes_from_user(self, user):
        return self.vote_dao.get_votes_from_user(user)

    def get_supporters_todays_choice(self, choice_of_the_day):
        """
        :param choice_of_the_day:
        :return: User that Voted for the Choice Of The Day
        """
        return self.vote_dao.get_supporters_todays_choice(choice_of_the_day)

    def choice_of_the_day(self):
        """
        :return: List with Restaurant_Names with most Votes
        """
        votes = self.vote_dao.get_all_votes()

        max_votes = votes.values('restaurant').annotate(restaurant_count=Count('restaurant')) \
            .aggregate(Max('restaurant_count')).get('restaurant_count__max')

        restaurant_ids = votes.values('restaurant') \
            .annotate(restaurant_count=Count('restaurant')) \
            .filter(restaurant_count=max_votes)

        return self.restaurant_logic.get_restaurants_with_ids(restaurant_ids)

    def save_vote_for_restaurants_with_names(self, restaurant_names, user):
        self.delete_votes_from_user(user)
        restaurants = self.restaurant_logic.get_restaurants_with_names(restaurant_names)
        for restaurant in restaurants:
            self.vote_dao.save_vote_for_restaurant_with_user(restaurant.get(), user)

    def delete_votes_from_user(self, user):
        self.vote_dao.delete_votes_from_user(user)

    def get_votes_for_restaurant_with_name(self, restaurant_name):
        return self.vote_dao.get_votes_for_restaurant_with_name(restaurant_name)
