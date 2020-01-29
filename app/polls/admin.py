from django.contrib import admin
from polls.models import Restaurant, Vote, Profile

admin.site.register([Restaurant, Vote, Profile])
