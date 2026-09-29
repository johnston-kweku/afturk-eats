from decimal import Decimal

def calculate_delivery_fee(item_count):
    """
    Temporary placeholder for delivery fee calculation.
    Real formula should factor in distance once Maps/geolocation is integrated.
    """
    base_fee = Decimal('10.00')
    if item_count > 3:
        return base_fee + Decimal('5.00')
    return base_fee