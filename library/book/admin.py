from django.contrib import admin
from book.models import Book


class BookIdFilter(admin.SimpleListFilter):
    title = 'Book ID'
    parameter_name = 'book_id'

    def lookups(self, request, model_admin):
        return [(book.id, f'#{book.id} — {book.name}') for book in Book.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id=self.value())
        return queryset


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'count', 'get_authors', 'is_available')
    list_filter = (BookIdFilter, 'name', 'authors')
    search_fields = ('name', 'authors__name', 'authors__surname')
    ordering = ('name',)

    fieldsets = (
        ('Book Info', {
            'description': 'Static information about the book',
            'fields': ('name', 'description')
        }),
        ('Availability', {
            'description': 'Dynamic data — changes when book is borrowed or returned',
            'fields': ('count',)
        }),
    )

    def get_authors(self, obj):
        return ', '.join([f'{a.name} {a.surname}' for a in obj.authors.all()])
    get_authors.short_description = 'Authors'

    def is_available(self, obj):
        return obj.count > 0
    is_available.boolean = True
    is_available.short_description = 'Available'