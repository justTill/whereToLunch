from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from polls.logic import SlackLogic
from utils.customize.models import Customize
from utils.enum import CustomizeChoices
from weather.models import Forecast


class SetUpTests(TestCase):
    slack = SlackLogic()

    def test_get_random_slack_message_with_users(self):
        message = self.slack.get_random_slack_message_with_users([])
        self.assertEqual(message, "congratulation all user have voted")

        user = User.objects.create(username='test_user', is_staff=True)
        user.set_password('12345')
        user.save()

        user.profile.slack_member_id = "12345"

        new_message = self.slack.get_random_slack_message_with_users([user])
        self.assertIn("12345", new_message)

    def test_send_vote_notification_to_slack_channel(self):
        Customize.objects.create(key_name=CustomizeChoices.SLACK_APP_API_KEY.value,
                                 string_property="hjgb")
        Customize.objects.create(key_name=CustomizeChoices.SLACK_CHANNEL.value,
                                 string_property="till")
        error = self.slack.send_vote_notification_to_slack_channel()
        self.assertRaises(Exception)

    def test_send_weather_forecast_to_slack_channel(self):
        Forecast.objects.create(temperature=12,
                                timestamp=timezone.now(),
                                weather_group="Snow",
                                description="description",
                                icon_id="1d")
        error = self.slack.send_weather_forecast_to_slack_channel()
        self.assertRaises(Exception)
