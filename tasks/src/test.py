from decimal import Decimal

from tasks.src.token_cost import calculate_cost


def test_calculate_cost():
    """
    Verify token cost calculation.
    """
    result = calculate_cost(
        token_count=1000,
        price_per_1000_tokens=Decimal("0.002"),
    )

    assert result == Decimal("0.002000")