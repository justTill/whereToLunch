from main.model.models import ChoicesOfTheWeek


class RestaurantStatisticsDAO:

    def get_restaurant_names(self):
        return ChoicesOfTheWeek.objects.all()

    def get_votes_for_restaurant(self, restaurant):
        return ChoicesOfTheWeek.objects.filter(restaurant_id=restaurant.get().id).count()
