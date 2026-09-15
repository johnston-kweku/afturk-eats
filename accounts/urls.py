from django.urls import path
from . import views



app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='home'),
    path('invite/', views.generate_invite_link, name='generate_invite_link'),
    path('invitation/', views.invite_link, name='invitation'),
    path('login/', views.login_view, name='login'),
    path('approval/pending/', views.pending_approval, name='pending_approval'),
    path('invite/invalid/', views.invalid_invite, name='invalid_invite'),
    path('register/', views.user_registration, name='user_registration'),
    path('logout/', views.logout_view, name='logout'),
    path('toggle/active/', views.toggle_online_status, name='toggle_status')
]