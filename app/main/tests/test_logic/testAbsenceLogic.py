import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from main.controller.logic import AbsenceLogic
from main.model.persistence import AbsenceDAO
from main.model.models import Absence
from users.models import Team
from utils.enum import Reasons
from utils.date import dateManager

User = get_user_model()


class AbsenceLogicTest(TestCase):
    absence_logic = AbsenceLogic()
    absence_dao = AbsenceDAO()

    today = dateManager.today()
    tomorrow = dateManager.tomorrow()
    yesterday = dateManager.today() + datetime.timedelta(days=-1)
    current_vote_date = dateManager.current_vote_day()

    def setUp(self):
        team = Team.objects.create(team_name="TestTeam")
        test_user = User.objects.create(username='test_user', is_staff=True)
        test_user.set_password('12345')
        test_user.team = team
        test_user.save()
        test_user_second = User.objects.create(username='test_user_second', is_staff=True)
        test_user_second.set_password('12345')
        test_user_second.team = team
        test_user_second.save()
        test_user_third = User.objects.create(username='test_user_third', is_staff=True)
        test_user_third.set_password('12345')
        test_user_third.team = team
        test_user_third.save()

        Absence.objects.create(user=test_user,
                               absenceFrom=self.today,
                               absenceTo=self.today,
                               reason=Reasons.OUT.value)
        Absence.objects.create(user=test_user_second,
                               absenceFrom=self.tomorrow,
                               absenceTo=self.tomorrow,
                               reason=Reasons.OUT.value)

        Absence.objects.create(user=test_user_third,
                               absenceFrom=self.yesterday,
                               absenceTo=self.yesterday,
                               reason=Reasons.OUT.value)
        # other User absence with different team does not effect absences for TestTeam
        other_team = Team.objects.create(team_name="other_team")
        other_user = User.objects.create(username='other_user', is_staff=True)
        other_user.set_password('12345')
        other_user.team = team
        Absence.objects.create(user=other_user,
                               absenceFrom=self.today,
                               absenceTo=self.today,
                               reason=Reasons.OUT.value)

    def test_check_if_a_absence_is_active_for_date(self):
        absence = [Absence.objects.get(user__username='test_user')]

        self.assertTrue(self.absence_logic.check_if_a_absence_is_active_for_date(absence, self.today))
        self.assertFalse(self.absence_logic.check_if_a_absence_is_active_for_date(absence, self.tomorrow))

    def test_delete_old_absence_for_user(self):
        absence_first_user = Absence.objects.get(user__username='test_user')
        absence_second_user = Absence.objects.get(user__username='test_user_second')
        firstUser = User.objects.get(username='test_user')
        secondUser = User.objects.get(username='test_user_second')

        self.absence_logic.delete_old_and_current_absences_for_user(firstUser)
        self.assertNotIn(absence_first_user, self.absence_dao.get_absences_from_user(firstUser))

        Absence.objects.create(user=firstUser,
                               absenceFrom=self.today,
                               absenceTo=self.today,
                               reason=Reasons.OUT.value)
        self.absence_logic.delete_old_and_current_absences_for_user(firstUser)
        self.assertIn(absence_second_user, self.absence_dao.get_absences_from_user(secondUser))

    def test_set_todays_absence_for_user(self):
        self.refresh_absence_databse()
        # User does not have any absence -> is after noon absence for tomorrow else for today / reason does not matter
        fresh_user = User.objects.create(username='fresh_user', is_staff=True)
        fresh_user.set_password('12345')
        fresh_user.save()

        self.absence_logic.set_vote_absence_for_user(user=fresh_user, reason=Reasons.OUT)
        absence_from_fresh_user = Absence.objects.filter(user=fresh_user)
        self.assertEqual(absence_from_fresh_user.get().absenceFrom, self.current_vote_date)
        self.absence_logic.set_vote_absence_for_user(user=fresh_user, reason=Reasons.OUT)
        absence_from_fresh_user = Absence.objects.filter(user=fresh_user)
        self.assertEqual(absence_from_fresh_user.filter(user=fresh_user).get().absenceFrom, self.current_vote_date)

        # Start with clear database
        self.refresh_absence_databse()
        self.absence_logic.set_vote_absence_for_user(user=fresh_user, reason=Reasons.OUT)
        out_absence = Absence.objects.get(user=fresh_user)
        self.absence_logic.set_vote_absence_for_user(user=fresh_user, reason=Reasons.DONOTCARE)
        all_absences = Absence.objects.all()
        # Old absence should be deleted
        self.assertNotIn(out_absence, all_absences)
        # New absence should be there
        do_not_care_absence = Absence.objects.get(user=fresh_user)
        self.assertIn(do_not_care_absence, all_absences)

    def test_delete_absences_for_user(self):
        absences = Absence.objects.all()
        self.assertEqual(len(absences), 4)
        for a in absences:
            self.absence_logic.delete_absences_for_user(a.user, [a.__str__()])

        absences = Absence.objects.all()
        self.assertEqual(len(absences), 0)

    def test_get_active_absent_absences(self):
        team = Team.objects.get(team_name="TestTeam")
        user = User.objects.get(username='test_user')
        absent = Absence.objects.create(user=user,
                                        absenceFrom=self.today,
                                        absenceTo=self.tomorrow,
                                        reason=Reasons.ABSENT.value)

        active_absences = self.absence_logic.get_active_absent_absences_from_team(team)
        self.assertEqual(active_absences, [absent])

    def test_delete_all_inactive_absences(self):
        first_absence = Absence.objects.get(user__username='test_user')
        second_absence = Absence.objects.get(user__username='test_user_second')
        third_absence = Absence.objects.get(user__username='test_user_third')
        other_absence = Absence.objects.get(user__username='other_user')

        self.assertEquals([first_absence, second_absence, third_absence, other_absence], list(Absence.objects.all()))
        self.absence_logic.delete_all_inactive_absences()
        self.assertIn(second_absence, list(Absence.objects.all()))

    def test_get_sorted_absent_absences(self):
        team = Team.objects.get(team_name="TestTeam")
        user = User.objects.get(username='test_user')
        user_two = User.objects.get(username='test_user_second')

        absence = Absence.objects.create(user=user,
                                         absenceFrom=self.today,
                                         absenceTo=self.today,
                                         reason=Reasons.ABSENT.value)
        absence_two = Absence.objects.create(user=user_two,
                                             absenceFrom=self.tomorrow,
                                             absenceTo=self.tomorrow,
                                             reason=Reasons.ABSENT.value)

        absences = self.absence_logic.get_sorted_absent_absences_for_team(team)
        self.assertEqual(absences, {'test_user': [absence], 'test_user_second': [absence_two]})

    def test_delete_vote_absence_for_user(self):
        self.refresh_absence_databse()
        user = User.objects.get(username='test_user')
        absence = Absence.objects.create(user=user,
                                         absenceFrom=self.today,
                                         absenceTo=self.today,
                                         reason=Reasons.OUT.value)

        self.absence_logic.delete_vote_absence_for_user(user, self.yesterday)
        self.assertEqual(list(Absence.objects.all()), [])

    def refresh_absence_databse(self):
        for a in Absence.objects.all():
            a.delete()
