import structlog
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from polls.logic import SlackLogic
from forecast import forecastApi
from utils import resetVotes, clearLogs
from customize.logic.customizeLogic import CustomizeLogic

logger = structlog.getLogger('cron')


def initialize_and_start_cron_jobs():
    # try catch block -> try access auf db if error take settings timezone
    # problem -> after update with db changes, need to re-save timezone
    # customize_logic = CustomizeLogic()
    # old_timezone = customize_logic.get_timezone()
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    create_and_start_cron_jobs_with_scheduler(scheduler)
    logger.info("initialized and started cron jobs with timezone: %s" % settings.TIME_ZONE)


def delete_old_and_create_new_cron_jobs_with_timezone(timezone):
    customize_logic = CustomizeLogic()
    old_timezone = customize_logic.get_timezone()
    old_scheduler = BackgroundScheduler(timezone=old_timezone)
    logger.info("delete old scheduler with old_timezone: %s" % old_timezone)
    delete_cron_jobs_for_scheduler(old_scheduler)

    new_scheduler = BackgroundScheduler(timezone=timezone)
    logger.info("create new scheduler: with new_timezone: %s" % timezone)
    create_and_start_cron_jobs_with_scheduler(new_scheduler)
    logger.info("new jobs from scheduler %s" % new_scheduler.get_jobs())


def create_and_start_cron_jobs_with_scheduler(scheduler):
    if isinstance(scheduler, BackgroundScheduler):
        slack = SlackLogic()
        scheduler.add_job(forecastApi.update_forecast, 'interval', minutes=20, id="update_forecast")
        scheduler.add_job(clearLogs.clear_debug_logs, 'interval', hours=1, id="clear_debug_logs")
        scheduler.add_job(clearLogs.clear_audit_logs, 'interval', hours=1, id="clear_audit_logs")
        scheduler.add_job(forecastApi.delete_old_forecasts, 'cron', hour=6, minute=00, id="delete_old_forecasts")
        scheduler.add_job(slack.send_vote_notification_to_slack_channel, 'cron', minute=00, hour=11, day_of_week="0-4",
                          id="send_vote_notification")
        scheduler.add_job(slack.send_weather_forecast_to_slack_channel, 'cron', minute=00, hour=15, day_of_week="0-4",
                          id="send_weather_forecast")
        scheduler.add_job(resetVotes.reset_things_from_last_vote_day, 'cron', minute=30, hour=12, day_of_week="0-4",
                          id="reset_things")
        scheduler.start()


def delete_cron_jobs_for_scheduler(scheduler):
    if isinstance(scheduler, BackgroundScheduler):
        scheduler.remove_all_jobs()
