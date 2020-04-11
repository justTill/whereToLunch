import datetime
from django import template
register = template.Library()


@register.filter()
def addDays(days):
    newDate = datetime.date.today() + datetime.timedelta(days=days)
    return newDate
