import requests
import structlog
from django.utils import timezone
from utils.date import dateManager
from main.model.models import Forecast
from main.controller.logic import CustomizeLogic

logger = structlog.getLogger(__name__)


def get_forecast_json():
    logger.debug("get things for weather forecast")
    customize_logic = CustomizeLogic()
    key = customize_logic.get_weather_api_key()
    city = customize_logic.get_city_for_weather()

    if key and city:
        url = 'http://api.openweathermap.org/data/2.5/forecast'
        r = requests.get('{0}?q={1}&APPID={2}'.format(
            url,
            city,
            key))

        try:
            r.raise_for_status()
            logger.debug("forecast json was successfully received")
            return r.json()
        except Exception as e:
            logger.error("something went wrong, is the city-name: (%s) or api-key (%s) correct ? ")
            logger.error("getting forecast causes following error: %s" % e)
            return None

    logger.warning("there is no api key or city name deposited")


def update_forecast():
    json = get_forecast_json()
    today = dateManager.today().strftime("%Y-%m-%d 12:00:00")
    tomorrow = dateManager.tomorrow().strftime("%Y-%m-%d 12:00:00")
    try:
        logger.debug("process forecast information in json")
        if json is not None:
            for json in json['list']:
                if json['dt_txt'] == tomorrow and dateManager.is_after_noon():
                    save_new_forecast(json)

                elif json['dt_txt'] == today and not dateManager.is_after_noon():
                    save_new_forecast(json)
    except:
        pass


def save_new_forecast(json):
    logger.debug("save forecast")
    new_forecast = Forecast()
    # open weather map gives temps in Kelvin. We want celsius.
    temp_in_celsius = json['main']['temp'] - 273.15
    new_forecast.temperature = temp_in_celsius
    new_forecast.description = json['weather'][0]['description']
    new_forecast.weather_group = json['weather'][0]['main']
    new_forecast.icon_id = json['weather'][0]['icon']
    new_forecast.save()


def delete_old_forecasts():
    dateManager.activate_timezone()
    Forecast.objects.filter(timestamp__lte=timezone.now()).delete()

