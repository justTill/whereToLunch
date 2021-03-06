from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from main.controller.logic import SlackLogic
from main.model.models import Customize, Forecast
from utils.enum import CustomizeChoices
from users.models import Team

User = get_user_model()


class SlackLogicTest(TestCase):
    slack = SlackLogic()

    def test_get_random_slack_message_with_users(self):
        message = self.slack.get_random_slack_message_with_users([])
        self.assertEqual(message, "congratulation all user have voted")

        user = User.objects.create(username='test_user', is_staff=True)
        user.set_password('12345')
        user.save()

        user.slack_member_id = "12345"

        new_message = self.slack.get_random_slack_message_with_users([user])
        self.assertIn("12345", new_message)

    def test_send_vote_notification_to_slack_channel(self):
        Customize.objects.create(key_name=CustomizeChoices.SLACK_APP_API_KEY.value,
                                 string_property="hjgb")
        Team.objects.create(team_name="testTeam",
                            slack_channel="till")
        self.slack.send_vote_notification_to_slack_channels()
        self.assertRaises(Exception)

    def test_send_weather_forecast_to_slack_channel(self):
        Forecast.objects.create(temperature=12,
                                timestamp=timezone.now(),
                                weather_group="Snow",
                                description="description",
                                icon_id="1d")
        error = self.slack.send_weather_forecast_to_slack_channels()
        self.assertRaises(Exception)
