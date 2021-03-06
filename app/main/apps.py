from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        # signals file is necessary for audit logs, so a logger can log if an object is about to be saved
        import signals
        from utils import crons
        crons.initialize_and_start_cron_jobs()
