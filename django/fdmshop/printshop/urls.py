# printshop/urls.py

from django.urls import path
from .views import filaments_view, product_filter_view, contact_view, add_product_view, register_view, login_view, logout_view, profile_view, change_password_view
from printshop.views import index_view

urlpatterns = [
    path('', index_view, name='index'),
    path('fdm-printers/',filaments_view,  name='filaments_view'),
    # path('products', product_filter_view, name='product_filter_view'),
    path('product-filter/', product_filter_view, name='product_filter'),
    path('contact/', contact_view, name='contact'),
    path('add-product/', add_product_view, name='add_product_view'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change-password/', change_password_view, name='change_password'),
]
