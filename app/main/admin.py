from django.contrib import admin
from .model.models import Absence
from .model.models import ChoicesOfTheWeek
from .model.models import Customize
from .model.models import Forecast
from .model.models import Restaurant, Vote, Profile


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register([Restaurant, Vote, Profile, ChoicesOfTheWeek, Forecast, Customize, Absence], ProfileAdmin)
