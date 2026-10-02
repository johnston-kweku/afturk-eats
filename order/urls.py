from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('cart/add/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
]