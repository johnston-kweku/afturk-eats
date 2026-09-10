from django.urls import path
from . import views


app_name = 'rider'
urlpatterns = [
    path('rider/dashboard/', views.rider_dashboard, name='rider_dashboard')
]