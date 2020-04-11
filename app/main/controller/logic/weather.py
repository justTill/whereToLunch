from main.model.models import Forecast


def weather_context():
    if Forecast.objects.all():
        latest_forecast = Forecast.objects.latest('timestamp')
        temperature_in_c = latest_forecast.temperature
        weather_group = latest_forecast.weather_group
        description = latest_forecast.description
        icon = latest_forecast.icon_id

        return {
            'temperature_in_c': temperature_in_c,
            'weather_group': weather_group,
            'description': description,
            'icon': icon
        }
    return {
        'temperature_in_c': '',
        'weather_group': '',
        'description': '',
        'icon': ''
    }
