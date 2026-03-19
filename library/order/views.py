import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from order.models import Order
from book.models import Book
from order.forms import EditOrderForm


@login_required
def order_list(request):
    if request.user.role != 1:
        return redirect('order:my_orders')
    orders = Order.objects.select_related('book', 'user').all()
    return render(request, 'order/order_list.html', {'orders': orders})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).select_related('book')
    return render(request, 'order/my_orders.html', {'orders': orders})


@login_required
def create_order(request, book_id):
    if request.user.role == 1:
        return redirect('book:list')

    book = get_object_or_404(Book, id=book_id)

    if book.count <= 0:
        return redirect('book:detail', book_id=book_id)

    if request.method == 'POST':
        plated_end_at_str = request.POST.get('plated_end_at')
        error = None

        try:
            plated_end_at = datetime.datetime.strptime(plated_end_at_str, '%Y-%m-%d').date()
            if plated_end_at <= datetime.date.today():
                error = 'Return date must be in the future.'
        except (ValueError, TypeError):
            error = 'Invalid date format.'

        if error:
            today = datetime.date.today()
            default_return = today + datetime.timedelta(days=14)
            return render(request, 'book/book_detail.html', {
                'book': book,
                'today': today,
                'default_return': default_return,
                'order_error': error,
            })

        Order.objects.create(
            book=book,
            user=request.user,
            created_at=datetime.datetime.now(),
            plated_end_at=datetime.datetime.combine(plated_end_at, datetime.time.min),
        )
        book.count -= 1
        book.save()
        return redirect('order:my_orders')

    return redirect('book:detail', book_id=book_id)


@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.user and request.user.role != 1:
        return redirect('order:my_orders')

    if order.end_at is not None:
        return redirect('order:my_orders')

    if request.method == 'POST':
        form = EditOrderForm(request.POST)
        if form.is_valid():
            plated_end_at = form.cleaned_data['plated_end_at']
            order.plated_end_at = datetime.datetime.combine(plated_end_at, datetime.time.min)
            order.save()
            return redirect('order:my_orders')
    else:
        form = EditOrderForm(initial={
            'plated_end_at': order.plated_end_at.date() if order.plated_end_at else None
        })

    return render(request, 'order/edit_order.html', {'order': order, 'form': form})


@login_required
def close_order(request, order_id):
    if request.user.role != 1:
        return redirect('order:my_orders')

    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.end_at = datetime.datetime.now()
        order.save()
        order.book.count += 1
        order.book.save()
        return redirect('order:order_list')

    return render(request, 'order/close_order.html', {'order': order})