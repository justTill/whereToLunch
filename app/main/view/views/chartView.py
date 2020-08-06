import structlog
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from main.controller.logic import RestaurantStatisticsLogic
from main.controller.logic import UserLogic

logger = structlog.getLogger(__name__)


class VotesChart(APIView):
    restaurant_statistics_logic = RestaurantStatisticsLogic()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = []
    user_logic = UserLogic()

    def get(self, request, Format=None):
        votesStatistic = {'restaurants_with_votes': []}
        team_name = self.request.query_params.get('team', None)
        if not request.user.is_anonymous and not team_name:
            team_name = request.user.team
        if team_name:
            logger.debug("get restaurants with votes for statistics")
            team = self.user_logic.get_team_with_name_or_none(team_name)
            if team:
                restaurants_with_votes = self.restaurant_statistics_logic.get_current_vote_statistics_data_for_team(team)
                votesStatistic.update({
                    'restaurants_with_votes': restaurants_with_votes,
                })
        return Response(votesStatistic)


class ChoicesChart(APIView):
    restaurant_statistics_logic = RestaurantStatisticsLogic()
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = []
    user_logic = UserLogic()

    def get(self, request, Format=None):
        choicesStatistic = {'choices_of_the_past': []}
        team_name = self.request.query_params.get('team', None)
        if not request.user.is_anonymous and not team_name:
            team_name = request.user.team
        if team_name:
            logger.debug("get choices of the past for statistics")
            team = self.user_logic.get_team_with_name_or_none(team_name)
            if team:
                get_choices_of_the_past = self.restaurant_statistics_logic.get_choices_of_the_past_from_team(team)
                choicesStatistic = {
                    'choices_of_the_past': get_choices_of_the_past
                }
        return Response(choicesStatistic)
