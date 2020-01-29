import datetime
from django.contrib.auth.models import User
from polls.tests import SetUpTests
from polls.logic import UserLogic


class UserLogicTest(SetUpTests):
    userLogic = UserLogic()
    today = datetime.date.today()

    def test_get_users_that_not_voted_yet(self):
        users = self.userLogic.get_users_that_not_voted_yet()
        for user in users:
            self.assertEquals(user, [])

        user = User.objects.create(username='user', is_staff=True)
        user.set_password('12345')
        user.save()
        users = self.userLogic.get_users_that_not_voted_yet()

        self.assertEquals(users.get(), user)

    def test_get_users_that_do_not_Care(self):
        user = User.objects.get(username='zweiter_test_user')

        users = self.userLogic.get_users_that_do_not_care()
        self.assertEquals(users, [user])

    def test_get_users_that_are_out(self):
        user = User.objects.get(username='vierter_test_user')
        users = self.userLogic.get_users_that_are_out()

        self.assertEquals(users, [user])

    def test_get_users_that_have_a_active_absent_absence(self):
        user = User.objects.get(username='erster_test_user')
        user_with_absence = self.userLogic.get_users_that_have_a_active_absent_absence()

        self.assertEquals(user_with_absence, [user])

    def test_get_user_that_are_not_available_for_lunch(self):
        not_available = self.userLogic.get_user_that_are_not_available_for_lunch()
        first_user = User.objects.get(username='erster_test_user')
        fourth_user = User.objects.get(username='vierter_test_user')

        self.assertEquals(not_available, [first_user, fourth_user])
