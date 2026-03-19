from django.contrib import admin
from authentication.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('id', 'email', 'first_name', 'last_name', 'middle_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('id',)

    fieldsets = (
        ('Account', {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'middle_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active')
        }),
    )