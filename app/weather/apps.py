from django.apps import AppConfig


class WeatherConfig(AppConfig):
    name = 'weather'

    def ready(self):
        from utils import update
        update.initialize_and_start_cron_jobs()
