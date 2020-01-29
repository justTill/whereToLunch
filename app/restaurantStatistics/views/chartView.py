from rest_framework.views import APIView
from rest_framework.response import Response
from restaurantStatistics.logic import RestaurantStatisticsLogic


class VotesChart(APIView):
    restaurant_statistics_logic = RestaurantStatisticsLogic()
    authentication_classes = []
    permission_classes = []

    def get(self, request, Format=None):
        restaurants_with_votes = self.restaurant_statistics_logic.get_current_vote_statistics_data()
        votesStatistic = {
            'restaurants_with_votes': restaurants_with_votes,
        }
        return Response(votesStatistic)


class ChoicesChart(APIView):
    restaurant_statistics_logic = RestaurantStatisticsLogic()
    authentication_classes = []
    permission_classes = []

    def get(self, request, Format=None):
        get_choices_of_the_past = self.restaurant_statistics_logic.get_choices_of_the_past()
        choicesStatistic = {
            'choices_of_the_past': get_choices_of_the_past
        }
        return Response(choicesStatistic)
