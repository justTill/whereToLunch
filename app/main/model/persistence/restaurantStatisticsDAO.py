from main.model.models import ChoicesOfTheWeek


class RestaurantStatisticsDAO:

    def get_restaurant_names_from_team(self, team):
        return ChoicesOfTheWeek.objects.all().select_related('restaurant').filter(restaurant__restaurant_for_team=team)

    def get_votes_for_restaurant(self, restaurant):
        return ChoicesOfTheWeek.objects.filter(restaurant_id=restaurant.get().id).count()
