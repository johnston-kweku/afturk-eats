from django.urls import path
from . import views



app_name = 'accounts'
urlpatterns = [
    path('landing/', views.home, name='home'),
    path('invite/', views.generate_invite_link, name='generate_invite_link'),
    path('login/', views.login_view, name='login'),
    path('approval/pending/', views.pending_approval, name='pending_approval'),
    path('invite/invalid/', views.invalid_invite, name='invalid_invite')
]