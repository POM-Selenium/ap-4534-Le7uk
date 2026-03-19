from django.contrib import admin
from author.models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'surname', 'patronymic', 'book_count')
    search_fields = ('name', 'surname')
    ordering = ('surname', 'name')

    fieldsets = (
        ('Name', {
            'fields': (('name', 'surname', 'patronymic'),)
        }),
        ('Books', {
            'fields': ('books',)
        }),
    )

    filter_horizontal = ('books',)

    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Books'