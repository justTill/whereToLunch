from django.conf import settings
from django.db import models
from utils.enum import CustomizeChoices


class Customize(models.Model):
    CHOICES = [
        (CustomizeChoices.WEBSITE_NAME.value, 'website_name'),
        (CustomizeChoices.BACKGROUND_IMAGE.value, 'background_image'),
        (CustomizeChoices.OPENWEATHERMAP_API_KEY.value, 'openweathermap_api_key'),
        (CustomizeChoices.SLACK_APP_API_KEY.value, 'slack_app_api_key'),
        (CustomizeChoices.SLACK_CHANNEL.value, 'slack_channel'),
        (CustomizeChoices.CITY_FOR_WEATHER.value, 'city_for_weather'),
        (CustomizeChoices.WEBSITE_URL.value, 'website_url'),
        (CustomizeChoices.TIMEZONE.value, 'timezone')
    ]
    key_name = models.CharField(choices=CHOICES, default=CHOICES, max_length=50, unique=True)
    string_property = models.CharField(max_length=500, null=True, blank=True)
    image_property = models.ImageField(upload_to='images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.key_name == CustomizeChoices.TIMEZONE.value:
            settings.TIME_ZONE = self.string_property
        super(Customize, self).save(*args, **kwargs)

    def __str__(self):
        return self.key_name
