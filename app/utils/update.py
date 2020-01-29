from apscheduler.schedulers.background import BackgroundScheduler
from polls.logic import SlackLogic
from forecast import forecastApi
from utils import resetVotes


def start():
    slack = SlackLogic()
    scheduler = BackgroundScheduler()

    scheduler.add_job(forecastApi.update_forecast, 'interval', minutes=20)
    scheduler.add_job(forecastApi.delete_old_forecasts, 'cron', hour=6, minute=00)
    scheduler.add_job(slack.send_vote_notification_to_slack_channel, 'cron', minute=00, hour=11, day_of_week="0-4")
    scheduler.add_job(slack.send_weather_forecast_to_slack_channel, 'cron', minute=00, hour=15, day_of_week="0-4")
    scheduler.add_job(resetVotes.reset_things_from_last_vote_day, 'cron', minute=40, hour=12, day_of_week="0-4")
    scheduler.start()
