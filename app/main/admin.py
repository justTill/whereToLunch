from django.contrib import admin
from .model.models import Customize
from .model.models import Absence
from .model.models import Forecast
from .model.models import ChoicesOfTheWeek
from .model.models import Restaurant, Vote, Profile


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register([Restaurant, Vote, Profile], ProfileAdmin)
admin.site.register([ChoicesOfTheWeek])
admin.site.register([Forecast])
admin.site.register([Customize])
admin.site.register([Absence])
