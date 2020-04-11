from pytz import timezone
from utils import crons
from unittest import TestCase
from customize.models.customize import Customize
from utils.enum import CustomizeChoices


class TestUpdate(TestCase):

    def setUp(self):
        Customize.objects.all().delete()

    def test_initialize_and_start_cron_jobs(self):
        scheduler = crons.initialize_and_start_cron_jobs()
        default_timezone = timezone('UTC')
        self.assertEqual(scheduler.timezone, default_timezone)

        Customize.objects.create(key_name=CustomizeChoices.TIMEZONE.value,
                                 string_property="Europe/Berlin")

        scheduler = crons.initialize_and_start_cron_jobs()
        changed_timezone = timezone("Europe/Berlin")
        self.assertEqual(scheduler.timezone, changed_timezone)

    def test_delete_old_and_create_new_cron_jobs_with_timezone(self):
        old_timezone = timezone('UTC')
        new_timezone = timezone('Europe/Berlin')
        schedulers = crons.delete_old_and_create_new_cron_jobs_with_timezone(new_timezone)
        old_scheduler = schedulers[0]
        new_scheduler = schedulers[1]
        self.assertEqual(old_scheduler.timezone, old_timezone)
        self.assertListEqual(old_scheduler.get_jobs(), [])
        self.assertEqual(new_scheduler.timezone, new_timezone)
        self.assertIsNot(new_scheduler.get_jobs(), [])
        self.assertEqual(len(new_scheduler.get_jobs()), 7)
