from django.db.models import Count
from main.model.models import Vote


class VoteDAO:

    def get_all_votes_from_team(self, team):
        return Vote.objects.all().select_related('user').select_related('restaurant').filter(user__team=team)

    def get_counted_votes(self, restaurant_id):
        votes = Vote.objects.all().filter(restaurant_id=restaurant_id)
        return votes.values('restaurant').annotate(restaurant_count=Count('restaurant'))

    def get_votes_from_user(self, user):
        return self.get_all_votes_from_team(user.team).filter(user=user)

    def get_supporters_for_restaurant(self, restaurant):
        votes = self.get_all_votes_from_team(restaurant.restaurant_for_team).filter(restaurant=restaurant)
        supporters = [vote.user.username for vote in votes]
        return supporters

    def save_vote_for_restaurant_with_user(self, restaurant, user):
        vote = Vote.objects.create(restaurant=restaurant, user=user)
        vote.save()
        vote.refresh_from_db()

    def delete_votes_from_user(self, user):
        self.get_all_votes_from_team(user.team).filter(user=user).delete()

    def get_votes_for_restaurant_with_name_for_team(self, restaurant_name, team):
        return self.get_all_votes_from_team(team).filter(restaurant__restaurant_name=restaurant_name).values('user__username')
