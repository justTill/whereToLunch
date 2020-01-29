import datetime
import requests

from django.utils import timezone
from weather.models import Forecast
from utils.date import dateManager
from utils.customize.logic import CustomizeLogic


def get_forecast_json():
    customize_logic = CustomizeLogic()
    key = customize_logic.get_weather_api_key()
    city = customize_logic.get_city_for_weather()
    if key and city:
        url = 'http://api.openweathermap.org/data/2.5/forecast'
        r = requests.get('{0}?q={1}&lang={2}&APPID={3}'.format(
            url,
            city,
            key))

        try:
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(e)
            return None


def update_forecast():
    json = get_forecast_json()
    today = timezone.now().strftime("%Y-%m-%d 12:00:00")
    tomorrow = timezone.now() + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime("%Y-%m-%d 12:00:00")
    try:
        if json is not None:
            for json in json['list']:
                if json['dt_txt'] == tomorrow and dateManager.is_after_noon():
                    save_new_forecast(json)

                elif json['dt_txt'] == today and not dateManager.is_after_noon():
                    save_new_forecast(json)

    except:
        pass


def save_new_forecast(json):
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

