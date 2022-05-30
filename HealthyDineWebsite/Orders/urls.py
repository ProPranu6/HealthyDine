from django.urls import path
from . import views
from .views import order_list, payment, add_to_cart, delete_from_cart, confirm_cart, extract_and_dump_food_interests, success_page

urlpatterns = [  
         path('order_list/', order_list, name='orders'),# app homepage
        path('payment/', payment, name="payments"),
        path('add_to_cart/', add_to_cart, name="cart-additions"),
        path('delete_from_cart/', delete_from_cart, name="cart-deletions"),
        path('confirm_cart/', confirm_cart, name='cart-confirmations'),
        path('extract_and_dump_food_interests/', extract_and_dump_food_interests, name='repalce-food-interests'),
        path('sucesspage/', success_page, name='payment-success')
]  