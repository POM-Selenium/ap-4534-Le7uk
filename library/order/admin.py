from django.contrib import admin
from order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ('id', 'book', 'user', 'created_at', 'plated_end_at', 'end_at', 'is_returned')
    list_filter = ('end_at', 'book', 'user')
    search_fields = ('book__name', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('-created_at',)

    fieldsets = (
        ('Order Info', {
            'description': 'Static data — set when order is created',
            'fields': ('book', 'user', 'created_at', 'plated_end_at')
        }),
        ('Return Info', {
            'description': 'Dynamic data — filled when book is returned',
            'fields': ('end_at',)
        }),
    )

    readonly_fields = ('created_at',)

    def is_returned(self, obj):
        return obj.end_at is not None
    is_returned.boolean = True
    is_returned.short_description = 'Returned'