from django.test import TestCase
from django.contrib.auth import get_user_model
from main.model.persistence import AbsenceDAO
from main.model.models import Absence
from users.models import Team
from utils.enum import Reasons
from utils.date import dateManager

User = get_user_model()


class AbsenceDaoTest(TestCase):
    absence_dao = AbsenceDAO()
    today = dateManager.today()

    def setUp(self):
        team = Team.objects.create(team_name="TestTeam")
        first_Test_User = User.objects.create(username='first_Test_User', is_staff=True)
        first_Test_User.set_password('12345')
        first_Test_User.team = team
        first_Test_User.save()

    def test_set_absence_for_User(self):
        user = User.objects.get(username='first_Test_User')

        self.absence_dao.set_absence_for_user(user, self.today, self.today, Reasons.ABSENT)
        user_absence = Absence.objects.filter(user=user,
                                              absenceFrom=self.today,
                                              absenceTo=self.today,
                                              reason=Reasons.ABSENT.value)

        self.assertEqual(len(user_absence), 1)

    def test_delete_absence(self):
        user = User.objects.get(username='first_Test_User')
        absence = Absence.objects.filter(user=user)
        self.absence_dao.delete_absence(absence)
        self.assertEqual(len(Absence.objects.all()), 0)

    def test_get_absences_from_user(self):
        user = User.objects.get(username='first_Test_User')
        Absence.objects.create(user=user,
                               absenceFrom=self.today,
                               absenceTo=self.today,
                               reason=Reasons.ABSENT.value)
        absences = Absence.objects.filter(user=user)
        self.assertEquals(len(absences), 1)

    def test_get_absences_for_reason(self):
        user = User.objects.get(username='first_Test_User')
        absence = Absence.objects.create(user=user,
                                         absenceFrom=self.today,
                                         absenceTo=self.today,
                                         reason=Reasons.ABSENT.value)
        absences_for_reason = self.absence_dao.get_absences_from_team_for_reason(Reasons.ABSENT, user.team)

        self.assertEqual(absence, absences_for_reason.get())
