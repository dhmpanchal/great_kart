from django.contrib import admin
from .models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html


class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_staff', 'is_admin', 'is_superadmin')
    list_display_links = ('email', 'first_name', 'last_name')
    list_filter = ('is_admin','is_active', 'is_staff', 'is_superadmin')
    search_fields = ('email',)
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'user', 'city', 'state', 'country', 'zip_code')
    readonly_fields = ('image_tag',)
    list_per_page = 10

# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)