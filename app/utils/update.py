from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from polls.logic import SlackLogic
from forecast import forecastApi
from utils import resetVotes, clearLogs
from customize.logic.customizeLogic import CustomizeLogic


def initialize_and_start_cron_jobs():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    create_and_start_cron_jobs_with_scheduler(scheduler)


def delete_old_and_create_new_cron_jobs_with_timezone(timezone):
    customize_logic = CustomizeLogic()
    old_scheduler = BackgroundScheduler(timezone=customize_logic.get_timezone())
    delete_cron_jobs_for_scheduler(old_scheduler)
    # only works one time not twice so the first time i change a timezone ist works if i changed it again ist does not work
    # build more log in save and update methods an watch logs
    new_scheduler = BackgroundScheduler(timezone=timezone)
    create_and_start_cron_jobs_with_scheduler(new_scheduler)


def create_and_start_cron_jobs_with_scheduler(scheduler):
    if isinstance(scheduler, BackgroundScheduler):
        slack = SlackLogic()
        scheduler.add_job(forecastApi.update_forecast, 'interval', minutes=20, id="update_forecast")
        scheduler.add_job(clearLogs.clear_debug_logs, 'interval', hours=1, id="clear_debug_logs")
        scheduler.add_job(clearLogs.clear_audit_logs, 'interval', hours=1, id="clear_audit_logs")
        scheduler.add_job(forecastApi.delete_old_forecasts, 'cron', hour=6, minute=00, id="delete_old_forecasts")
        scheduler.add_job(slack.send_vote_notification_to_slack_channel, 'cron', minute=00, hour=11, day_of_week="0-4", id="send_vote_notification")
        scheduler.add_job(slack.send_weather_forecast_to_slack_channel, 'cron', minute=00, hour=15, day_of_week="0-4", id="send_weather_forecast")
        scheduler.add_job(resetVotes.reset_things_from_last_vote_day, 'cron', minute=30, hour=12, day_of_week="0-4", id="reset_things")
        scheduler.start()


def delete_cron_jobs_for_scheduler(scheduler):
    if isinstance(scheduler, BackgroundScheduler):
        scheduler.remove_all_jobs()
