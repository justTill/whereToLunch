import random
from slacker import Slacker
from polls.logic import UserLogic
from weather.logic import weather_context
from utils.customize.logic import CustomizeLogic


class SlackLogic:
    userLogic = UserLogic()
    customize_logic = CustomizeLogic()

    def get_random_slack_message_with_users(self, slack_users):
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

        return "Super es haben alle Auserwählten abgestimmt"

    def send_vote_notification_to_slack_channel(self):
        user_that_voted = self.userLogic.get_users_that_not_voted_yet()
        message = self.get_random_slack_message_with_users(user_that_voted)

        self.send_message_to_slack_channel(message)

    def send_weather_forecast_to_slack_channel(self):
        current_weather_forecast = weather_context()
        bad_weather_groups = {'Thunderstorm', 'Drizzle', 'Rain', 'Snow'}

        if current_weather_forecast.get('weather_group') in bad_weather_groups:
            message = "Das morgige Wetter ist nicht ganz so gut :( " \
                      "\nDie Genauen Wetteraussichten sehen wie folgt aus: " \
                      "\nTemperatur: * {temp}°C* " \
                      "\nBeschreibung: *{desc}* " \
                      "\nJetzt Abstimmen!!!!" \
                .format(temp=current_weather_forecast.get('temperature_in_c').__str__(),
                        desc=current_weather_forecast.get('description'))

            self.send_message_to_slack_channel(message)

    def send_message_to_slack_channel(self, message):
        api_key = self.customize_logic.get_slack_api_key()
        channel_name = self.customize_logic.get_slack_channel_name()
        if api_key and channel_name:
            try:
                slack = Slacker(api_key)
                slack.chat.post_message(channel_name, message)
            except Exception as e:
                print(e)
