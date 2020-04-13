from django.contrib import admin
from .model.models import Absence, ChoicesOfTheWeek, Customize, Forecast, Restaurant, Vote, Profile, Team


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register([Restaurant, Vote, Profile, ChoicesOfTheWeek, Forecast, Customize, Absence, Team], ProfileAdmin)
