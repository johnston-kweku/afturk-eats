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