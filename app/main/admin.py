from django.contrib import admin
from main.model.models import Absence, ChoicesOfTheWeek, Customize, Forecast, Restaurant, Vote


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register([Restaurant, Vote, ChoicesOfTheWeek, Forecast, Customize, Absence], ProfileAdmin)
