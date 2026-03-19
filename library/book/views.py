from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from book.models import Book
from order.models import Order
from book.forms import BookForm
import datetime


def book_list(request):
    books = Book.objects.prefetch_related('authors').all()
    return render(request, 'book/book_list.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    today = datetime.date.today()
    default_return = today + datetime.timedelta(days=14)
    user_has_order = False
    if request.user.is_authenticated:
        user_has_order = Order.objects.filter(
            book=book, user=request.user, end_at__isnull=True
        ).exists()
    return render(request, 'book/book_detail.html', {
        'book': book,
        'today': today,
        'default_return': default_return,
        'user_has_order': user_has_order,
    })


def books_by_user(request, user_id):
    orders = Order.objects.filter(user_id=user_id).select_related('book')
    books = [o.book for o in orders]
    return render(request, 'book/books_by_user.html', {'books': books})


@login_required
def create_book(request):
    if request.user.role != 1:
        return redirect('book:list')

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('book:detail', book_id=book.id)
    else:
        form = BookForm()

    return render(request, 'book/book_form.html', {'form': form, 'action': 'Create'})


@login_required
def edit_book(request, book_id):
    if request.user.role != 1:
        return redirect('book:list')

    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book:detail', book_id=book.id)
    else:
        form = BookForm(instance=book)

    return render(request, 'book/book_form.html', {'form': form, 'action': 'Edit', 'book': book})


@login_required
def delete_book(request, book_id):
    if request.user.role != 1:
        return redirect('book:list')

    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book:list')
    return render(request, 'book/delete_book.html', {'book': book})