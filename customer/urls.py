from django.urls import path
from . import views


app_name = 'customer'
urlpatterns = [
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard')
]