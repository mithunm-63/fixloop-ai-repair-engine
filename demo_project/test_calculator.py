from calculator import calculate_total

def test_total_without_discount():
    assert calculate_total([{"price": 10, "quantity": 2}]) == 20

def test_percentage_discount():
    assert calculate_total([{"price": 100, "quantity": 1}], discount=10) == 90

def test_discount_on_larger_subtotal():
    assert calculate_total([{"price": 200, "quantity": 1}], discount=10) == 180

def test_zero_discount():
    assert calculate_total([{"price": 7, "quantity": 3}], discount=0) == 21
