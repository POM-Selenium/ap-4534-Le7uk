from django.shortcuts import render
from book.models import Book
from author.models import Author
from order.models import Order


def home_view(request):
    book_count = Book.objects.count()
    author_count = Author.objects.count()
    available_count = Book.objects.filter(count__gt=0).count()
    active_orders = Order.objects.filter(end_at=None).count()
    recent_books = Book.objects.prefetch_related('authors').order_by('-id')[:6]

    return render(request, 'home.html', {
        'book_count': book_count,
        'author_count': author_count,
        'available_count': available_count,
        'active_orders': active_orders,
        'recent_books': recent_books,
    })