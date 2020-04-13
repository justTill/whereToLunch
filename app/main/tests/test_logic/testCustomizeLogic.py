from unittest import TestCase
from main.model.models import Customize
from main.controller.logic import CustomizeLogic
from utils.enum import CustomizeChoices


class TestCustomizeLogic(TestCase):
    customize_logic = CustomizeLogic()

    def setUp(self):
        Customize.objects.all().delete()
        Customize.objects.create(key_name=CustomizeChoices.WEBSITE_URL.value,
                                 string_property="website_url")
        Customize.objects.create(key_name=CustomizeChoices.WEBSITE_NAME.value,
                                 string_property="website_name")
        Customize.objects.create(key_name=CustomizeChoices.CITY_FOR_WEATHER.value,
                                 string_property="city_for_weather")
        Customize.objects.create(key_name=CustomizeChoices.SLACK_CHANNEL.value,
                                 string_property="slack_channel")
        Customize.objects.create(key_name=CustomizeChoices.OPENWEATHERMAP_API_KEY.value,
                                 string_property="weather_key")
        Customize.objects.create(key_name=CustomizeChoices.BACKGROUND_IMAGE.value,
                                 image_property="background_image")

    def test_get_different_customizes(self):
        self.assertEqual(self.customize_logic.get_slack_api_key(), "")
        Customize.objects.create(key_name=CustomizeChoices.SLACK_APP_API_KEY.value,
                                 string_property="slack_key")
        self.assertEqual(self.customize_logic.get_slack_api_key(), "slack_key")
        self.assertEqual(self.customize_logic.get_website_name(), "website_name")
        self.assertEqual(self.customize_logic.get_weather_api_key(), "weather_key")
        self.assertEqual(self.customize_logic.get_background_image_url(), "/mediafiles/background_image")
        self.assertEqual(self.customize_logic.get_slack_channel_name(), "slack_channel")
        self.assertEqual(self.customize_logic.get_city_for_weather(), "city_for_weather")
        self.assertEqual(self.customize_logic.get_website_url(), "website_url")
        self.assertEqual(self.customize_logic.get_timezone(), "UTC")
        Customize.objects.create(key_name=CustomizeChoices.TIMEZONE.value,
                                 string_property="Europe/Berlin")
        self.assertEqual(self.customize_logic.get_timezone(), "Europe/Berlin")
