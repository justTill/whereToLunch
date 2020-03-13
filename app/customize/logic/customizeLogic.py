import structlog
from customize.persistence import CustomizeDAO
from utils.enum import CustomizeChoices

logger = structlog.getLogger(__name__)


class CustomizeLogic:
    customize_dao = CustomizeDAO()

    def get_slack_api_key(self):
        slack_key_object = self.customize_dao.get_customize_field_for_choice(CustomizeChoices.SLACK_APP_API_KEY)
        return self.get_customize_string_property(slack_key_object)

    def get_website_name(self):
        name_object = self.customize_dao.get_customize_field_for_choice(CustomizeChoices.WEBSITE_NAME)
        name = self.get_customize_string_property(name_object)
        return name if name else ' Where To Eat ? '

    def get_weather_api_key(self):
        weather_key_object = self.customize_dao.get_customize_field_for_choice(CustomizeChoices.OPENWEATHERMAP_API_KEY)
        return self.get_customize_string_property(weather_key_object)

    def get_slack_channel_name(self):
        slack_channel_object = self.customize_dao.get_customize_field_for_choice(CustomizeChoices.SLACK_CHANNEL)
        return self.get_customize_string_property(slack_channel_object)

    def get_city_for_weather(self):
        city_object = self.customize_dao.get_customize_field_for_choice(CustomizeChoices.CITY_FOR_WEATHER)
        return self.get_customize_string_property(city_object)

    def get_website_url(self):
        website_object = self.customize_dao.get_customize_field_for_choice(CustomizeChoices.WEBSITE_URL)
        return self.get_customize_string_property(website_object)

    def get_timezone(self):
        noon_time_object = self.customize_dao.get_customize_field_for_choice(CustomizeChoices.TIMEZONE)
        return self.get_customize_string_property(noon_time_object)

    def get_background_image_url(self):
        image_object = self.customize_dao.get_customize_field_for_choice(CustomizeChoices.BACKGROUND_IMAGE)
        logger.debug("try to get image property from customize: %s" % image_object)
        if image_object and image_object.get().image_property:
            return image_object.get().image_property.url
        logger.warn("Image property is not there for customize: %s" % image_object)
        return ''

    def get_customize_string_property(self, customize):
        logger.debug("get string property from customize: %s" % customize)
        if customize and customize.get().string_property:
            return customize.get().string_property
        logger.warn("String property is not there for customize: %s" % customize)
        return ''
