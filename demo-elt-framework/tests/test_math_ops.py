from demo_elt_framework.math_ops import add, subtract, divide
import math
import pytest

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(10, 7) == 3

def test_divide():
    assert divide(10, 2) == 5.0

def test_divide_zero_raise():
    with pytest.raises(Exception):
        divide(1, 0)

def test_divide_zero_inf():
    assert math.isinf(divide(1, 0, on_zero="inf"))

def test_divide_zero_nan():
    assert math.isnan(divide(0, 0, on_zero="nan"))
