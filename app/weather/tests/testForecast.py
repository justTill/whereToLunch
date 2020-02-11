import datetime
import forecast
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from weather.models import Forecast
from weather.logic import weather_context
from customize.models import Customize
from utils.enum import CustomizeChoices


class SetUpTests(TestCase):
    first_forecast = {"cod": "200", "message": 0.0032, "cnt": 36, "list": [
            {"dt": 1487257200,
             "main": {"temp": 285.66, "temp_min": 281.821,
                   "temp_max": 285.66, "pressure": 970.91,
                   "sea_level": 1044.32,
                   "grnd_level": 970.91, "humidity": 70,
                   "temp_kf": 3.84},
             "weather": [{"id": 800, "main": "Clear",
                       "description": "clear sky",
                       "icon": "01d"}],
             "clouds": {"all": 0},
             "wind": {"speed": 1.59, "deg": 290.501},
             "sys": {"pod": "d"},
             "dt_txt": "2017-02-16 15:00:00"},
            {"dt": 1487624400,
             "main": {"temp": 272.424, "temp_min": 272.424,
                    "temp_max": 272.424, "pressure": 968.38,
                    "sea_level": 1043.17,
                    "grnd_level": 968.38, "humidity": 85,
                    "temp_kf": 0},
             "weather": [{"id": 801, "main": "Clouds",
                        "description": "few clouds",
                        "icon": "02n"}],
             "clouds": {"all": 20},
             "wind": {"speed": 3.57, "deg": 255.503},
             "rain": {}, "snow": {}, "sys": {"pod": "n"},
             "dt_txt": "2017-02-20 21:00:00"}],
         "city": {"id": 6940463, "name": "Altstadt", "coord": {"lat": 48.137, "lon": 11.5752},
                     "country": "none"}}

    second_forecast = {"cod": "200", "message": 0.0032, "cnt": 36, "list": [],
             "city": {"id": 6940463, "name": "Altstadt", "coord": {"lat": 48.137, "lon": 11.5752},
                      "country": "none"}}

    def test_safe_new_fore_cast(self):
        for json in self.first_forecast['list']:
            forecast.save_new_forecast(json)
        assert len(Forecast.objects.all()), 2

    def test_weather_context(self):
        current_forecast = weather_context()
        self.assertEqual(current_forecast, {'temperature_in_c': '', 'weather_group': '', 'description': '', 'icon': ''})
        timestamp = timezone.now() + datetime.timedelta(hours=1)
        Forecast.objects.create(timestamp=timestamp, temperature=120.42, description='sunny', icon_id='01d')
        context = weather_context()
        self.assertEquals(context['temperature_in_c'], Decimal('120.42'))
        self.assertEquals(context['description'], 'sunny')
        self.assertEquals(context['icon'], '01d')

    def test_get_forecast_json(self):

        Customize.objects.create(key_name=CustomizeChoices.OPENWEATHERMAP_API_KEY.value,
                                 string_property="jhgjhg",
                                 )
        Customize.objects.create(key_name=CustomizeChoices.CITY_FOR_WEATHER.value,
                                 string_property="Cologne",
                                 )
        response = forecast.get_forecast_json()
        self.assertRaises(Exception, response)
        self.assertEqual(response, None)
