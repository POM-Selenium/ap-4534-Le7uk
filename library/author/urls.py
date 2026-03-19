from django.urls import path
from author import views

app_name = 'author'

urlpatterns = [
    path('', views.all_authors, name='list'),
    path('create/', views.create_author, name='create'),
    path('delete/<int:author_id>/', views.delete_author, name='delete'),
]