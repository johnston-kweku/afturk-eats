from vendor.models import MenuItemVariant


class Cart:
    def __init__(self, request, vendor_id):
        self.session = request.session
        self.vendor_id = str(vendor_id)
        self.carts = self.session.setdefault('carts', {})
        self.cart = self.carts.get(self.vendor_id, {})

    @staticmethod
    def vendor_ids(request):
        return list(request.session.get('carts', {}).keys())

    def add(self, variant_id, quantity=1):
        variant_id = str(variant_id)
        self.cart[variant_id] = self.cart.get(variant_id, 0) + quantity
        self._save()

    def remove(self, variant_id):
        self.cart.pop(str(variant_id), None)
        self._save()

    def update_quantity(self, variant_id, quantity):
        variant_id = str(variant_id)
        if variant_id not in self.cart:
            return
        if quantity <= 0:
            self.cart.pop(variant_id)
        else:
            self.cart[variant_id] = quantity
        self._save()

    def clear(self):
        self.cart.clear()
        self._save()

    def _save(self):
        if self.cart:
            self.carts[self.vendor_id] = self.cart
        else:
            self.carts.pop(self.vendor_id, None)
        self.session.modified = True

    def __len__(self):
        return sum(self.cart.values())

    def __iter__(self):
        variants = (
            MenuItemVariant.objects
            .filter(id__in=self.cart.keys())
            .select_related('menu_item', 'menu_item__vendor')
        )
        for variant in variants:
            quantity = self.cart[str(variant.id)]
            yield {
                'variant': variant,
                'quantity': quantity,
                'line_total': variant.price * quantity,
            }

    def get_subtotal(self):
        return sum(entry['line_total'] for entry in self)