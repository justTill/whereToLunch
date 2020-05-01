import structlog
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.db import OperationalError, ProgrammingError
from main.controller.logic import SlackLogic, CustomizeLogic
from main.controller.forecast import forecastApi
from utils import resetVotes, clearLogs

logger = structlog.getLogger('cron')


def initialize_and_start_cron_jobs():
    customize_logic = CustomizeLogic()
    try:
        timezone = customize_logic.get_timezone()
    except ProgrammingError:
        logger.warn("could not get timezone from database")
        logger.info("use default timezone from settings")
        timezone = settings.TIME_ZONE
    except OperationalError:
        logger.warn("could not get timezone from database")
        logger.info("use default timezone from settings")
        timezone = settings.TIME_ZONE
    scheduler = BackgroundScheduler(timezone=timezone)
    create_and_start_cron_jobs_with_scheduler(scheduler)
    logger.info("initialized and started cron jobs with timezone: %s" % timezone)
    return scheduler


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
    return [old_scheduler, new_scheduler]


def create_and_start_cron_jobs_with_scheduler(scheduler):
    if isinstance(scheduler, BackgroundScheduler):
        slack = SlackLogic()
        scheduler.add_job(forecastApi.update_forecast, 'interval', minutes=20, id="update_forecast")
        scheduler.add_job(clearLogs.clear_debug_logs, 'interval', minutes=23, id="clear_debug_logs")
        scheduler.add_job(clearLogs.clear_audit_logs, 'interval', minutes=23, id="clear_audit_logs")
        scheduler.add_job(forecastApi.delete_old_forecasts, 'cron', hour=6, minute=00, id="delete_old_forecasts")
        scheduler.add_job(slack.send_vote_notification_to_slack_channels, 'cron', minute=00, hour=11, day_of_week="0-4",
                          id="send_vote_notification")
        scheduler.add_job(slack.send_weather_forecast_to_slack_channels, 'cron', minute=00, hour=15, day_of_week="0-4",
                          id="send_weather_forecast")
        scheduler.add_job(resetVotes.reset_things_from_last_vote_day, 'cron', minute=30, hour=12, day_of_week="0-4",
                          id="reset_things")
        scheduler.start()


def delete_cron_jobs_for_scheduler(scheduler):
    if isinstance(scheduler, BackgroundScheduler):
        scheduler.remove_all_jobs()
