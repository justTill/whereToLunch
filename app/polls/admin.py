from django.contrib import admin
from polls.models import Restaurant, Vote, Profile


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register([Restaurant, Vote, Profile], ProfileAdmin)
