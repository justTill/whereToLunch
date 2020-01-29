from django.db.models.functions import Lower
from polls.models import Restaurant


class RestaurantDAO:

    def get_all_restaurants(self):
        """
        :return Queryset of all Restaurants
        """
        return Restaurant.objects.order_by(Lower('restaurant_name'))

    def get_restaurants_with_ids(self, restaurant_ids):
        """
        :param restaurant_ids: from restaurants you wants to get
        :return: Restaurants with given ids
        """
        restaurants = [
            Restaurant.objects.get(pk=id.get('restaurant'))
            for id in restaurant_ids
        ]
        return restaurants

    def get_restaurant_with_name(self, restaurant_name):
        return Restaurant.objects.filter(restaurant_name=restaurant_name)

    def get_color_for_restaurant_with_name(self, restaurant_name):
        return Restaurant.objects.filter(restaurant_name=restaurant_name).get().restaurant_color

