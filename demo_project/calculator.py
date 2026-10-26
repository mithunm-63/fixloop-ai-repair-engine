def calculate_total(items, discount=0):
    """Return the total price after applying a discount percentage."""
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    # BUG: discount is a percentage, but this subtracts the raw number.
    return subtotal - discount
