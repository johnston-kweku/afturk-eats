from django.urls import path
from . import views


app_name = 'customer'
urlpatterns = [
    path('/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('settings/', views.customer_settings, name='settings')
]