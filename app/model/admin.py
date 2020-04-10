from django.contrib import admin
from customize.models import Customize
from absenceCalendar.models import Absence
from weather.models import Forecast
from restaurantStatistics.models import ChoicesOfTheWeek
from polls.models import Restaurant, Vote, Profile


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register([Restaurant, Vote, Profile], ProfileAdmin)
admin.site.register([ChoicesOfTheWeek])
admin.site.register([Forecast])
admin.site.register([Customize])
admin.site.register([Absence])
