from django.urls import path
from . import views


app_name = 'vendor'
urlpatterns = [
    path('vendor/dasboard/', views.vendor_dashboard, name='vendor_dashboard')
]