from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from author.models import Author
from author.forms import AuthorModelForm


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
def all_authors(request):
    authors = Author.objects.prefetch_related("books").all()
    return render(request, "author/all_authors.html", {"authors": authors})


@librarian_required
def create_author(request):
    form = AuthorModelForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            author = form.save()
            messages.success(
                request, f"Author {author.name} {author.surname} created successfully"
            )
            return redirect("/authors/")
        messages.error(request, "Please correct the errors below.")

    return render(request, "author/create_author.html", {"form": form})


@librarian_required
def delete_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)

    if author.books.count() > 0:
        messages.error(
            request,
            f"Cannot delete {author.name} {author.surname} — they have {author.books.count()} book(s) attached.",
        )
        return redirect("/authors/")

    if request.method == "POST":
        name = f"{author.name} {author.surname}"
        Author.delete_by_id(author_id)
        messages.success(request, f"Author {name} deleted successfully")
        return redirect("/authors/")

    return render(request, "author/delete_author.html", {"author": author})
