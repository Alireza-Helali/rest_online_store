from django.contrib import admin
from .models import Address, Supplier, User, Profile
from django.contrib.auth.admin import UserAdmin as BaseAdmin


class UserAdmin(BaseAdmin):
    ordering = ('id',)
    list_display = ['email', 'name']
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('name',),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Important dates', {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }
         ),
    )


admin.site.register(Address)
admin.site.register(Supplier)
admin.site.register(Profile)
admin.site.register(User, UserAdmin)
