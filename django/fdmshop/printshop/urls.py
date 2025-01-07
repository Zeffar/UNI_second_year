# printshop/urls.py

from django.urls import path
from .views import filaments_view, product_filter_view, contact_view, add_product_view, register_view, login_view, logout_view, profile_view, change_password_view
from printshop.views import index_view, virtual_basket_view, remove_from_basket, increment_quantity, decrement_quantity, add_to_basket, update_quantity
from . import views

urlpatterns = [
    path('', index_view, name='index'),
    path('filaments-view/',filaments_view,  name='filaments_view'),
    path('products', product_filter_view, name='product_filter_view'),
    path('product-filter/', product_filter_view, name='product_filter'),
    path('contact/', contact_view, name='contact'),
    path('add-product/', add_product_view, name='add_product_view'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change-password/', change_password_view, name='change_password'),
    path('basket/add/<int:product_id>/', add_to_basket, name='add_to_basket'),
    path('basket/update/<int:item_id>/', update_quantity, name='update_quantity'),
    path('basket/remove/<int:item_id>/', remove_from_basket, name='remove_from_basket'),
     path('basket/increment/<int:item_id>/', increment_quantity, name='increment_quantity'),
    path('basket/decrement/<int:item_id>/', decrement_quantity, name='decrement_quantity'),
    path('virtual-basket/', virtual_basket_view, name='virtual_basket'),
]
