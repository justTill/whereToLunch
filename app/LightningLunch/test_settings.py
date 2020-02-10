import datetime
from LightningLunch.settings import *

DJANGO_ALLOWED_HOSTS = ['*']
SECRET_KEY = 'I AM SECRET'
RESET_VOTES_MIN = int((datetime.datetime.now() + datetime.timedelta(minutes=1)).minute)
RESET_VOTES_HOUR = int(datetime.datetime.now().hour)
