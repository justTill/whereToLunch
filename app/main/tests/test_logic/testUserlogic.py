import datetime
from django.test import TestCase
from main.controller.logic import UserLogic
from main.model.models import Vote, Absence
from utils.enum import Reasons
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLogicTest(TestCase):
    userLogic = UserLogic()
    today = datetime.date.today()

    def setUp(self):
        first_test_user = User.objects.create(username='first_test_user', is_staff=True)
        first_test_user.set_password('12345')
        first_test_user.save()

        Absence.objects.create(user=first_test_user,
                               absenceFrom=self.today,
                               absenceTo=self.today + datetime.timedelta(days=1),
                               reason=Reasons.ABSENT.value
                               )

        second_test_user = User.objects.create(username='second_test_user', is_staff=True)
        second_test_user.set_password('12345')
        second_test_user.save()

        Absence.objects.create(user=second_test_user,
                               absenceFrom=self.today,
                               absenceTo=self.today + datetime.timedelta(days=1),
                               reason=Reasons.DONOTCARE.value
                               )

        third_test_user = User.objects.create(username='third_test_user', is_staff=True)
        third_test_user.set_password('12345')
        third_test_user.save()

        Absence.objects.create(user=third_test_user,
                               absenceFrom=self.today,
                               absenceTo=self.today,
                               reason=Reasons.OUT.value
                               )

    def test_get_users_that_not_voted_yet(self):
        User.objects.all().delete()
        self.assertFalse(self.userLogic.get_users_from_team_that_not_voted_yet().exists())
        user = User.objects.create(username='user', is_staff=True)
        user.set_password('12345')
        user.save()
        users = self.userLogic.get_users_from_team_that_not_voted_yet()

        self.assertEquals(users.get(), user)

    def test_get_users_that_do_not_Care(self):
        user = User.objects.get(username='second_test_user')
        users = self.userLogic.get_users_from_team_that_do_not_care()
        self.assertEquals(users, [user])

    def test_get_users_that_are_out(self):
        user = User.objects.get(username='third_test_user')
        users = self.userLogic.get_users_from_team_that_are_out()

        self.assertEquals(users, [user])

    def test_get_users_that_have_a_active_absent_absence(self):
        user = User.objects.get(username='first_test_user')
        user_with_absence = self.userLogic.get_users_from_team_that_have_a_active_absent_absence()

        self.assertEquals(user_with_absence, [user])

    def test_get_user_that_are_not_available_for_lunch(self):
        not_available = self.userLogic.get_user_from_team_that_are_not_available_for_lunch()
        first_user = User.objects.get(username='first_test_user')
        third_user = User.objects.get(username='third_test_user')

        self.assertEquals(not_available, [first_user, third_user])
