# order/views.py
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from accounts.decorators import role_required
from accounts.models import User
from vendor.models import MenuItemVariant
from .cart import Cart

MAX_QUANTITY = 20


@require_POST
@role_required(User.Role.CUSTOMER)
def add_to_cart(request, variant_id):
    variant = MenuItemVariant.objects.select_related('menu_item__vendor').filter(id=variant_id).first()
    if variant is None:
        return JsonResponse({'success': False, 'message': 'Item not found.'}, status=404)

    if not variant.is_available or not variant.menu_item.is_available or not variant.menu_item.vendor.is_online:
        return JsonResponse({'success': False, 'message': 'This item is no longer available.'}, status=400)

    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'success': False, 'message': 'Invalid quantity.'}, status=400)

    if quantity < 1 or quantity > MAX_QUANTITY:
        return JsonResponse({'success': False, 'message': f'Quantity must be between 1 and {MAX_QUANTITY}.'}, status=400)

    cart = Cart(request, variant.menu_item.vendor.id)
    cart.add(variant.id, quantity)

    return JsonResponse({
        'success': True,
        'message': f'{variant.menu_item.name} ({variant.label}) added to cart.',
        'cart_count': len(cart),
    })






from django.contrib import messages
from django.shortcuts import render, redirect
from vendor.models import VendorProfile


@role_required(User.Role.CUSTOMER)
def cart_page(request):
    carts = []
    for vendor_id in Cart.vendor_ids(request):
        vendor = VendorProfile.objects.filter(id=vendor_id).first()
        if vendor is None:
            continue

        entries = list(Cart(request, vendor_id))
        if not entries:
            continue

        carts.append({
            'vendor': vendor,
            'entries': entries,
            'item_count': sum(e['quantity'] for e in entries),
            'subtotal': sum(e['line_total'] for e in entries),
            'orderable': vendor.is_online and all(
                e['variant'].is_available and e['variant'].menu_item.is_available
                for e in entries
            ),
        })

    return render(request, 'order/cart.html', {'carts': carts})


@require_POST
@role_required(User.Role.CUSTOMER)
def update_cart_item(request, vendor_id, variant_id):
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        messages.error(request, 'Invalid quantity.')
        return redirect('order:cart')

    quantity = min(quantity, MAX_QUANTITY)
    Cart(request, vendor_id).update_quantity(variant_id, quantity)
    return redirect('order:cart')


@require_POST
@role_required(User.Role.CUSTOMER)
def remove_cart_item(request, vendor_id, variant_id):
    Cart(request, vendor_id).remove(variant_id)
    return redirect('order:cart')


@require_POST
@role_required(User.Role.CUSTOMER)
def clear_cart(request, vendor_id):
    Cart(request, vendor_id).clear()
    messages.success(request, 'Cart cleared.')
    return redirect('order:cart')