import structlog
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from main.controller.logic import RestaurantStatisticsLogic

logger = structlog.getLogger(__name__)


class VotesChart(APIView):
    restaurant_statistics_logic = RestaurantStatisticsLogic()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, Format=None):
        team = request.user.team
        logger.debug("get restaurants with votes for statistics")
        restaurants_with_votes = self.restaurant_statistics_logic.get_current_vote_statistics_data_for_team(team)
        votesStatistic = {
            'restaurants_with_votes': restaurants_with_votes,
        }
        return Response(votesStatistic)


class ChoicesChart(APIView):
    restaurant_statistics_logic = RestaurantStatisticsLogic()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, Format=None):
        team = request.user.team
        logger.debug("get choices of the past for statistics")
        get_choices_of_the_past = self.restaurant_statistics_logic.get_choices_of_the_past_from_team(team)
        choicesStatistic = {
            'choices_of_the_past': get_choices_of_the_past
        }
        return Response(choicesStatistic)
