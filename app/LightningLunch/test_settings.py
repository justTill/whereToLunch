import datetime
from LightningLunch.settings import *

RESET_VOTES_MIN = int((datetime.datetime.now() + datetime.timedelta(minutes=1)).minute)
RESET_VOTES_HOUR = int(datetime.datetime.now().hour)
