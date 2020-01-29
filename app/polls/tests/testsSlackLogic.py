from django.contrib.auth.models import User
from django.test import TestCase
from polls.logic import SlackLogic
from polls.models import Profile


class SetUpTests(TestCase):

    def test_get_random_slack_message_with_users(self):
        slack = SlackLogic()
        message = slack.get_random_slack_message_with_users([])
        self.assertEqual(message, "Super es haben alle Auserwählten abgestimmt")

        user = User.objects.create(username='test_user', is_staff=True)
        user.set_password('12345')
        user.save()

        user.profile.slack_member_id = "12345"

        new_message = slack.get_random_slack_message_with_users([user])
        self.assertIn("12345", new_message)
