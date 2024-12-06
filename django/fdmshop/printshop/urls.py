# printshop/urls.py

from django.urls import path
from .views import filaments_view, product_filter_view, contact_view, add_product_view

urlpatterns = [
    # Other URL patterns...
    path('fdm-printers/',filaments_view,  name='filaments_view'),
    path('products', product_filter_view, name='product_filter_view'),
    path('product-filter/', product_filter_view, name='product_filter'),
    path('contact/', contact_view, name='contact'),
    path('add-product/', add_product_view, name='add_product_view'),
]
