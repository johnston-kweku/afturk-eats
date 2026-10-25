from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('cart/add/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart'),
    path('cart/<int:vendor_id>/update/<int:variant_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/<int:vendor_id>/remove/<int:variant_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('cart/<int:vendor_id>/clear/', views.clear_cart, name='clear_cart'),
]