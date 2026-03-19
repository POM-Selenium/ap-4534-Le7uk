from django.urls import path
from order import views

app_name = 'order'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('my/', views.my_orders, name='my_orders'),
    path('create/<int:book_id>/', views.create_order, name='create_order'),
    path('edit/<int:order_id>/', views.edit_order, name='edit_order'),
    path('close/<int:order_id>/', views.close_order, name='close_order'),
]