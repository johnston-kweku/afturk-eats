from django.shortcuts import render
from accounts.decorators import role_required
from accounts.models import User
from vendor.models import Category, VendorProfile, MenuItem, MenuItemVariant
from order.models import Order, OrderItem

# Create your views here.

@role_required(User.Role.CUSTOMER)
def customer_dashboard(request):
    menu_items = MenuItem.objects.all().prefetch_related(
        'variants'
    )
    categories = Category.objects.all()
    context = {
        'menu_items': menu_items,
        'categories': categories
    }
    if request.method == 'POST':
        items_filter = request.POST.get('filter', '')
        if not items_filter:
            error = 'Please provide a filter'
            context['error'] = error
            return render(request, 'customer/customer_dashboard', context)

        menu_items = MenuItem.objects.filter(category=items_filter).prefetch_related('variants')
        context['menu_items'] = menu_items
    return render(request, 'customer/customer_dashboard.html', context)



@role_required(User.Role.CUSTOMER)
def customer_settings(request):
    return render(request, 'customer/settings.html')