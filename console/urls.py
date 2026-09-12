from django.urls import path
from . import views 


app_name = 'console'
urlpatterns = [
    path('console/dashboard/', views.admin_dashboard, name='admin_dashboard' )
]