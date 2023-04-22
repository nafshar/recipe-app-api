"""
Django Admin Customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# The following import will show an error in IDE
# However we need to ignore this error as we run this
# odule inside a Docker Container which uses a different
# path settings to get to the "core" module and "models" file.
from core import models


class UserAdmin(BaseUserAdmin):
    """ Define the admin pages for users """
    ordering = ['id']
    list_display = ['email', 'name']


admin.site.register(models.User, UserAdmin)
