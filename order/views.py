from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import role_required
from accounts.models import User
from vendor.models import MenuItemVariant
from .cart import Cart


@role_required(User.Role.CUSTOMER)
def add_to_cart(request, variant_id):
    if request.method != 'POST':
        return redirect('customer:customer_dashboard')

    variant = get_object_or_404(
        MenuItemVariant.objects.select_related('menu_item__vendor'),
        id=variant_id
    )

    if not variant.is_available or not variant.menu_item.vendor.is_online:
        messages.error(request, 'This item is no longer available.')
        return redirect('customer:customer_dashboard')

    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    vendor_id = variant.menu_item.vendor.id
    cart = Cart(request, vendor_id)
    cart.add(variant_id, quantity)

    messages.success(request, f'{variant.menu_item.name} ({variant.label}) added to cart.')
    return redirect('customer:customer_dashboard')