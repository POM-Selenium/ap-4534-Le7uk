from django.urls import path
from book import views

app_name = 'book'

urlpatterns = [
    path('', views.book_list, name='list'),
    path('create/', views.create_book, name='create'),
    path('<int:book_id>/', views.book_detail, name='detail'),
    path('<int:book_id>/edit/', views.edit_book, name='edit'),
    path('<int:book_id>/delete/', views.delete_book, name='delete'),
    path('user/<int:user_id>/', views.books_by_user, name='by_user'),
]