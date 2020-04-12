import datetime
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from main.model.models import Absence, Forecast
from utils.enum import Reasons
from utils.date import dateManager


class AbsenceIndexTest(TestCase):
    today = dateManager.today()
    tomorrow = dateManager.tomorrow()
    yesterday = today + datetime.timedelta(days=-1)

    def setUp(self):
        Forecast.objects.create(temperature=12, description="sunny")

        another_test_user = User.objects.create(username='another_test_user', is_staff=True)
        another_test_user.set_password('12345')
        another_test_user.save()

        Absence.objects.create(user=another_test_user,
                               absenceFrom=self.tomorrow,
                               absenceTo=self.tomorrow,
                               reason=Reasons.ABSENT.value
                               )

    def test_absenceIndex(self):
        absence = Absence.objects.get(user__username='another_test_user')
        response = self.client.get(reverse('main:absenceIndex'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context[-1]['weather_context'],
                          {'temperature_in_c': Decimal('12.00'),
                           'weather_group': '',
                           'description': 'sunny',
                           'icon': ''})
        self.assertEquals(response.context[-1]['absences_from_users'], {'another_test_user': [absence]})

    def test_save_new_absence(self):
        user = User.objects.get(username='another_test_user')
        self.assertEqual(len(Absence.objects.all()), 1)

        login = self.client.post('/admin/login/?next=/save_new_absence', {'username': 'another_test_user', 'password': '12345'})
        self.assertRedirects(login, '/save_new_absence', status_code=302)
        response = self.client.post('/save_new_absence', {'user': user, 'absenceFrom': self.today, 'absenceTo': self.today})
        self.assertEqual(len(Absence.objects.all()), 2)
        response = self.client.post('/save_new_absence', {'user': user, 'absenceFrom': self.yesterday, 'absenceTo': self.yesterday})
        self.assertEqual(len(Absence.objects.all()), 2)

    def test_delete_absences(self):
        user = User.objects.get(username='another_test_user')
        absence = Absence.objects.get(user__username='another_test_user')

        self.assertEqual(Absence.objects.all().get(), absence)
        self.assertEqual(len(Absence.objects.all()), 1)

        login = self.client.post('/admin/login/?next=/delete_absences', {'username': 'another_test_user', 'password': '12345'})
        self.assertRedirects(login, '/delete_absences', status_code=302, target_status_code=302)

        response = self.client.post('/delete_absences', {'user': user, 'absenceBox': absence.__str__()})

        self.assertEqual(len(Absence.objects.all()), 0)


