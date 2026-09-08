from django.urls import path
from . import views



app_name = 'accounts'
urlpatterns = [
    path('invite/', views.generate_invite_link, name='generate_invite_link')
]