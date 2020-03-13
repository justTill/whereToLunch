import datetime

import pytz
from django.utils import timezone
from customize.logic.customizeLogic import CustomizeLogic

customizeLogic = CustomizeLogic()


def today():
    activate_timezone()
    return timezone.now().date()


def tomorrow():
    activate_timezone()
    return timezone.now().date() + datetime.timedelta(days=1)


def is_after_noon():
    activate_timezone()
    now = timezone.localtime(timezone.now())
    now = now.time().strftime('%H:%M')
    noon = timezone.now().time().replace(hour=12, minute=30, second=0).strftime('%H:%M')
    return now >= noon


def current_vote_day():
    return tomorrow() if is_after_noon() else today()


def activate_timezone():
    time_zone = customizeLogic.get_timezone()
    if time_zone:
        timezone.activate(pytz.timezone(time_zone))
