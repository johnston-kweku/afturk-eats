from vendor.models import MenuItemVariant


class Cart:
    def __init__(self, request, vendor_id):
        self.session = request.session
        self.vendor_id = str(vendor_id)

        carts = self.session.get('carts')
        if carts is None:
            carts = self.session['carts'] = {}

        cart = carts.get(self.vendor_id)
        if cart is None:
            cart = carts[self.vendor_id] = {}

        self.carts = carts
        self.cart = cart

    def add(self, variant_id, quantity=1):
        variant_id = str(variant_id)
        current_quantity = self.cart.get(variant_id, 0)
        self.cart[variant_id] = current_quantity + quantity
        self.save()

    def remove(self, variant_id):
        variant_id = str(variant_id)
        if variant_id in self.cart:
            del self.cart[variant_id]
            self.save()

    def update_quantity(self, variant_id, quantity):
        variant_id = str(variant_id)
        if quantity <= 0:
            self.remove(variant_id)
            return
        self.cart[variant_id] = quantity
        self.save()

    def clear(self):
        if self.vendor_id in self.carts:
            del self.carts[self.vendor_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        return sum(self.cart.values())

    def __iter__(self):
        variant_ids = self.cart.keys()
        variants = MenuItemVariant.objects.filter(id__in=variant_ids).select_related('menu_item', 'menu_item__vendor')

        for variant in variants:
            quantity = self.cart[str(variant.id)]
            yield {
                'variant': variant,
                'quantity': quantity,
                'line_total': variant.price * quantity,
            }

    def get_subtotal(self):
        return sum(entry['line_total'] for entry in self)