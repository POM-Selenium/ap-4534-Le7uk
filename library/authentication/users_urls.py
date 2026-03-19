from django.urls import path
from authentication import views

app_name = 'users'

urlpatterns = [
    path('', views.all_users, name='list'),
    path('<int:user_id>/', views.user_detail, name='detail'),
]