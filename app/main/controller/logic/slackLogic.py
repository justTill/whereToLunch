import random
import structlog
from slacker import Slacker
from .userLogic import UserLogic
from .weather import weather_context
from .customizeLogic import CustomizeLogic
from users.models import Team

logger = structlog.getLogger(__name__)


class SlackLogic:
    userLogic = UserLogic()
    customize_logic = CustomizeLogic()

    def get_random_slack_message_with_users(self, slack_users):
        logger.debug('get random slack message')
        member_ids = ""
        if slack_users:
            for user in slack_users:
                if user.slack_member_id:
                    member_ids = member_ids + "<@" + user.slack_member_id + "> "
            if member_ids:
                switcher = {
                    1: member_ids + "are to slow. They do not get any kind of food today",
                    2: "NO FOOD FOR " + member_ids,
                    3: "Following users need to vote " + member_ids,
                    4: "shame shame shame shame shame shame " + member_ids + " shame shame shame shame shame shame",
                    5: member_ids + "are on a diet, so no food for them, not even a crumb of bread."
                }
                return switcher.get(random.randint(1, 5), "Following users need to vote " + member_ids) \
                       + " Vote NOW !!! "
        logger.debug('no user is left, all have voted')
        return "congratulation all user have voted"

    def get_weather_forecast(self):
        logger.debug('get weather information and check if a message should be send')
        current_weather_forecast = weather_context()
        bad_weather_groups = {'Thunderstorm', 'Drizzle', 'Rain', 'Snow'}

        if current_weather_forecast.get('weather_group') in bad_weather_groups:
            logger.debug('send message')
            message = "The weather forecast for tomorrow is not that good :( " \
                      "\nThe exact weather forecast looks as follows: " \
                      "\nTemperatur: * {temp}°C* " \
                      "\nDescription: *{desc}* " \
                      "\nVote Now!!!!" \
                .format(temp=current_weather_forecast.get('temperature_in_c').__str__(),
                        desc=current_weather_forecast.get('description'))
            url = self.customize_logic.get_website_url()
            return message + " " + url
        else:
            return ""

    def send_vote_notification_to_slack_channels(self):
        logger.debug('send notification to slack channel')
        url = self.customize_logic.get_website_url()
        for team in Team.objects.all():
            user_that_not_voted = self.userLogic.get_users_from_team_that_not_voted_yet(team)
            message = self.get_random_slack_message_with_users(user_that_not_voted)
            slack_channel = team.slack_channel
            self.send_message_to_slack_channel(slack_channel, message + " " + url)

    def send_weather_forecast_to_slack_channels(self):
        url = self.customize_logic.get_website_url()
        for team in Team.objects.all():
            slack_channel = team.slack_channel
            if slack_channel:
                message = self.get_weather_forecast()
                if message:
                    self.send_message_to_slack_channel(slack_channel, message + " " + url)

    def send_message_to_slack_channel(self, slack_channel, message):
        logger.debug('send message: %s to slack channel' % message)
        api_key = self.customize_logic.get_slack_api_key()
        if api_key and slack_channel:
            try:
                logger.debug('try to send message')
                slack = Slacker(api_key)
                slack.chat.post_message(slack_channel, message)
                logger.debug('successful sending of a message')
            except Exception as e:
                logger.error('something went wrong, is the api_key correct (%s)? and the channel name (%s)?'
                             % (api_key, slack_channel))
                logger.error('trying to send a notification caused following error %s' % e)
        else:
            logger.warning('there is no api Key and/or channel_name')
