from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from account.models import User, Course, Subscriber, Video, Contact
from django.contrib.auth.models import Group


class UserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'number', 'date_joined',
                    'last_login', 'is_admin', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
         'fields': ('first_name', 'last_name', 'number', 'photo')}),
        ('Permissions', {'fields': ('is_admin',
                                    'is_staff', 'is_superuser', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullnamd', 'phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'phone',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Contact)
admin.site.register(Video)
admin.site.register(Subscriber)
admin.site.unregister(Group)
