from django.urls import path
from . import views


app_name = 'vendor'
urlpatterns = [
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('add/menu-item/', views.add_menu_item, name='add_menu_item'),
    path('edit/menu-item/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('menu/', views.vendor_menu, name='vendor_menu'),
    path('menu/item/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('toggle/available/<int:item_id>/', views.toggle_item_availability, name='toggle_item_availability'),
    path('settings/', views.vendor_settings, name='settings'),
    path('edit/opening-hours/', views.vendor_opening_hours, name='edit_opening_hours')
]