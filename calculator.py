def calculate_total(price, discount):
    """Return price after a percentage discount."""
    if price < 0:
        raise ValueError("price cannot be negative")
    if discount < 0 or discount > 100:
        raise ValueError("discount must be between 0 and 100")
    return price - discount
