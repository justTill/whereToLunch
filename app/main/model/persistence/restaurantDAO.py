from django.db.models.functions import Lower
from main.model.models import Restaurant


class RestaurantDAO:

    def get_all_restaurants_from_team(self, team):
        return Restaurant.objects.filter(restaurant_for_team=team).order_by(Lower('restaurant_name'))

    def get_restaurants_with_ids(self, restaurant_ids):
        restaurants = [
            Restaurant.objects.get(pk=id.get('restaurant'))
            for id in restaurant_ids
        ]
        return restaurants

    def get_restaurant_with_name_for_team(self, restaurant_name, team):
        return Restaurant.objects.filter(restaurant_name=restaurant_name).filter(restaurant_for_team=team)

    def get_color_for_restaurant_with_name_for_team(self, restaurant_name, team):
        return Restaurant.objects.filter(restaurant_name=restaurant_name).filter(restaurant_for_team=team).get().restaurant_color
