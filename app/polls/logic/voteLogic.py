import structlog
from django.db.models import Count, Max
from polls.persistence import VoteDAO
from polls.logic import RestaurantLogic

logger = structlog.getLogger(__name__)


class VoteLogic:
    vote_dao = VoteDAO()
    restaurant_logic = RestaurantLogic()

    def get_votes_from_user(self, user):
        logger.info('get votes from user: %s' % user.username)
        return self.vote_dao.get_votes_from_user(user)

    def get_supporters_for_restaurant(self, restaurant):
        logger.info('get supporters for restaurant: %s' % restaurant)
        return self.vote_dao.get_supporters_for_restaurant(restaurant)

    def choice_of_the_day(self):
        votes = self.vote_dao.get_all_votes()
        logger.info('calculate/get restaurant with the most votes')

        max_votes = votes.values('restaurant').annotate(restaurant_count=Count('restaurant')) \
            .aggregate(Max('restaurant_count')).get('restaurant_count__max')

        restaurant_ids = votes.values('restaurant') \
            .annotate(restaurant_count=Count('restaurant')) \
            .filter(restaurant_count=max_votes)

        return self.restaurant_logic.get_restaurants_with_ids(restaurant_ids)

    def save_vote_for_restaurants_with_names(self, restaurant_names, user):
        logger.info('save restaurants: %s for user: %s' % (restaurant_names, user))
        self.delete_votes_from_user(user)
        restaurants = self.restaurant_logic.get_restaurants_with_names(restaurant_names)
        for restaurant in restaurants:
            self.vote_dao.save_vote_for_restaurant_with_user(restaurant.get(), user)

    def delete_votes_from_user(self, user):
        logger.info('delete vote from user: %s' % user)
        self.vote_dao.delete_votes_from_user(user)

    def get_votes_for_restaurant_with_name(self, restaurant_name):
        logger.info('how many votes does this restaurant: %s have ?' % restaurant_name)
        return self.vote_dao.get_votes_for_restaurant_with_name(restaurant_name)

    def get_voted_restaurants_from_user(self, user):
        logger.info('get votes from user: %s' % user)
        voted_restaurants = [vote.restaurant for vote in self.get_votes_from_user(user)]
        return voted_restaurants

    def get_choice_of_the_day_supporters(self, choice_of_the_day):
        logger.info('get supporter for choice of the day: %s' % choice_of_the_day)
        supporters = []
        if len(choice_of_the_day) == 1:
            supporters = self.get_supporters_for_restaurant(choice_of_the_day[0])
        return supporters
