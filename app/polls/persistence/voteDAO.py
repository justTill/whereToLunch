from django.db.models import Count
from polls.models import Vote


class VoteDAO:

    def get_all_votes(self):
        return Vote.objects.all().select_related('user').select_related('restaurant')

    def get_counted_votes(self):
        votes = self.get_all_votes()
        return votes.values('restaurant').annotate(restaurant_count=Count('restaurant'))

    def get_votes_from_user(self, user):
        return self.get_all_votes().filter(user=user)

    def get_supporters_todays_choice(self, choice_of_the_day):
        votes = self.get_all_votes().filter(restaurant=choice_of_the_day[0])
        supporters = [vote.user.username for vote in votes]
        return supporters

    def save_vote_for_restaurant_with_user(self, restaurant, user):
        vote = Vote.objects.create(restaurant=restaurant, user=user)
        vote.save()
        vote.refresh_from_db()

    def delete_votes_from_user(self, user):
        self.get_all_votes().filter(user=user).delete()

    def get_votes_for_restaurant_with_name(self, restaurant_name):
        return self.get_all_votes().filter(restaurant__restaurant_name=restaurant_name).values('user__username')
