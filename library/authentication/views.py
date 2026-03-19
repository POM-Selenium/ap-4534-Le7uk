from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages

from authentication.models import CustomUser
from authentication.forms import CustomUserModelForm, LoginUserForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("/books/")

    form = CustomUserModelForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome, {user.first_name}!")
        return redirect("/books/")

    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/books/")

    form = LoginUserForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("/books/")

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/auth/login/")


def librarian_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/auth/login/")
        if request.user.role != 1:
            messages.error(request, "Access denied. Librarians only.")
            return redirect("/books/")
        return view_func(request, *args, **kwargs)

    return wrapper


@librarian_required
def all_users(request):
    users = CustomUser.objects.all().order_by("last_name", "first_name")
    return render(request, "auth/all_users.html", {"users": users})


@librarian_required
def user_detail(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)
    from order.models import Order

    orders = (
        Order.objects.filter(user=target_user)
        .select_related("book")
        .order_by("-created_at")
    )
    return render(
        request,
        "auth/user_detail.html",
        {
            "target_user": target_user,
            "orders": orders,
        },
    )
