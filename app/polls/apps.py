from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'polls'

    def ready(self):
        # signals file is necessary for audit logs, so a logger can log if an object is about to be saved
        import signals
        from utils import update
        update.initialize_and_start_cron_jobs()
