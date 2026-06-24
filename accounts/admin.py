from django.contrib import admin
from .models import Account

from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active')
    list_display_links = ('email','username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
