import datetime
from django.utils import timezone


def today():
    return datetime.date.today()


def tomorrow():
    return today() + datetime.timedelta(days=1)


def is_after_noon():
    now = timezone.now() + datetime.timedelta(hours=1)
    now = now.time().strftime('%H:%M')
    noon = timezone.now().time().replace(hour=12, minute=30, second=0).strftime('%H:%M')
    return now >= noon


def current_vote_day():
    return tomorrow() if is_after_noon() else today()
