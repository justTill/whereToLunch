import datetime
import requests
import structlog

from django.utils import timezone
from weather.models import Forecast
from utils.date import dateManager
from utils.customize.logic import CustomizeLogic

logger = structlog.getLogger(__name__)


def get_forecast_json():
    logger.info("get things for weather forecast")
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
            logger.info("forecast json was successfully received")
            return r.json()
        except Exception as e:
            logger.ERROR("something went wrong, is the city-name: (%s) or api-key (%s) correct ? ")
            print(e)
            return None

    logger.warn("there is no api key or city name deposited")


def update_forecast():
    json = get_forecast_json()
    today = timezone.now().strftime("%Y-%m-%d 12:00:00")
    tomorrow = timezone.now() + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime("%Y-%m-%d 12:00:00")
    try:
        logger.info("check if json has the right format")
        if json is not None:
            for json in json['list']:
                if json['dt_txt'] == tomorrow and dateManager.is_after_noon():
                    save_new_forecast(json)

                elif json['dt_txt'] == today and not dateManager.is_after_noon():
                    save_new_forecast(json)
    except:
        pass


def save_new_forecast(json):
    logger.info("save forecast")
    new_forecast = Forecast()
    # open weather map gives temps in Kelvin. We want celsius.
    temp_in_celsius = json['main']['temp'] - 273.15
    new_forecast.temperature = temp_in_celsius
    new_forecast.description = json['weather'][0]['description']
    new_forecast.weather_group = json['weather'][0]['main']
    new_forecast.icon_id = json['weather'][0]['icon']
    new_forecast.save()


def delete_old_forecasts():
    # timzeone.now equals the actual date minus one hour
    Forecast.objects.filter(timestamp__lte=timezone.now()).delete()

