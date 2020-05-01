from django.contrib import admin
from .models import User, Team
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


UserAdmin.fieldsets = ((None, {'fields': ('username', 'password')}),
                       (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'team', 'slack_member_id', 'user_image',)}), (
                           _('Permissions'),
                           {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                       (_('Important dates'), {'fields': ('last_login',)}))

admin.site.register(User, UserAdmin)
admin.site.register(Team)
