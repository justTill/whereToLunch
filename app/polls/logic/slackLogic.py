import random
import structlog
from slacker import Slacker
from polls.logic import UserLogic
from weather.logic import weather_context
from utils.customize.logic import CustomizeLogic

logger = structlog.getLogger(__name__)


class SlackLogic:
    userLogic = UserLogic()
    customize_logic = CustomizeLogic()

    def get_random_slack_message_with_users(self, slack_users):
        logger.info('get random slack message')
        member_ids = ""
        if slack_users:
            for user in slack_users:
                if user.profile.slack_member_id:
                    member_ids = member_ids + "<@" + user.profile.slack_member_id + "> "
            if member_ids:
                switcher = {
                    1: "Die Schnecken des Tages heißen: " + member_ids,
                    2: "ES GIBT HEUTE KEIN ESSEN FÜR " + member_ids,
                    3: "Essen fällt für " + member_ids + "aus",
                    4: "shame shame shame shame shame shame " + member_ids + " shame shame shame shame shame shame",
                    5: member_ids + "machen eine Diät, daher bekommen sie heute nichts zum Essen."
                }
                return switcher.get(random.randint(1, 5), "Folgende Personen sollten noch Abstimmen " + member_ids) \
                       + " Jetzt abstimmen !!! "
        logger.info('no user is left, all have voted')
        return "Super es haben alle Auserwählten abgestimmt"

    def send_vote_notification_to_slack_channel(self):
        logger.info('send notification to slack channel')
        user_that_voted = self.userLogic.get_users_that_not_voted_yet()
        message = self.get_random_slack_message_with_users(user_that_voted)
        url = self.customize_logic.get_website_url()

        self.send_message_to_slack_channel(message + " " + url)

    def send_weather_forecast_to_slack_channel(self):
        logger.info('process weather information and check if a message should be send')
        current_weather_forecast = weather_context()
        bad_weather_groups = {'Thunderstorm', 'Drizzle', 'Rain', 'Snow'}

        if current_weather_forecast.get('weather_group') in bad_weather_groups:
            logger.info('send message')
            message = "Das morgige Wetter ist nicht ganz so gut :( " \
                      "\nDie Genauen Wetteraussichten sehen wie folgt aus: " \
                      "\nTemperatur: * {temp}°C* " \
                      "\nBeschreibung: *{desc}* " \
                      "\nJetzt Abstimmen!!!!" \
                .format(temp=current_weather_forecast.get('temperature_in_c').__str__(),
                        desc=current_weather_forecast.get('description'))
            url = self.customize_logic.get_website_url()

            self.send_message_to_slack_channel(message + " " + url)

    def send_message_to_slack_channel(self, message):
        logger.info('send message: %s to slack channel' % message)
        api_key = self.customize_logic.get_slack_api_key()
        channel_name = self.customize_logic.get_slack_channel_name()
        if api_key and channel_name:
            try:
                logger.info('try to send message')
                slack = Slacker(api_key)
                slack.chat.post_message(channel_name, message)
                logger.info('successful sending of a message')
            except Exception as e:
                logger.error('something went wrong, is the api_key correct (%s)? and the channel name (%s)?'
                               % (api_key, channel_name))
                logger.error('trying to send a notification caused following error %s' % e)
        else:
            logger.warning('there is no api Key and/or channel_name')
