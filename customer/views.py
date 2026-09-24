from django.shortcuts import render
from accounts.decorators import role_required
from accounts.models import User
from vendor.models import Category, VendorProfile, MenuItem, MenuItemVariant
from order.models import Order, OrderItem

# Create your views here.

@role_required(User.Role.CUSTOMER)
def customer_dashboard(request):
    menu_items = MenuItem.objects.filter(is_available=True, vendor__is_online=True).prefetch_related(
        'variants'
    )
    categories = Category.objects.all()
    context = {
        'menu_items': menu_items,
        'categories': categories
    }

    items_filter = request.GET.get('category', '')

    if items_filter:
        menu_items = menu_items.filter(category__name=items_filter)
        context['menu_items'] = menu_items
        return render(request, 'customer/customer_dashboard.html', context)

    context['menu_items'] = menu_items
    return render(request, 'customer/customer_dashboard.html', context)



@role_required(User.Role.CUSTOMER)
def customer_settings(request):
    return render(request, 'customer/settings.html')