import datetime

from django.test import TestCase
from absenceCalendar.forms import AbsenceForm
from utils.date import dateManager


class AbsenceFromTest(TestCase):
    today = dateManager.today()
    tomorrow = dateManager.tomorrow()
    yesterday = today + datetime.timedelta(days=-1)

    def test_absence_form(self):
        form_data = {'absenceFrom': self.today, 'absenceTo': self.tomorrow}
        form = AbsenceForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {'absenceFrom': self.tomorrow, 'absenceTo': self.today}
        form = AbsenceForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'absenceFrom': self.tomorrow, 'absenceTo': self.yesterday}
        form = AbsenceForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'absenceFrom': self.yesterday, 'absenceTo': self.today}
        form = AbsenceForm(data=form_data)
        self.assertFalse(form.is_valid())
