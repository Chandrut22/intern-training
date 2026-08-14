from decimal import Decimal


def calculate_cost(
    token_count: int,
    price_per_1000_tokens: Decimal = Decimal("0.002"),
    currency: str = "$",
    precision: int = 6,
) -> Decimal:
    """
    Calculate the cost for a given number of tokens.

    Args:
        token_count: Number of tokens.
        price_per_1000_tokens: Price charged per 1000 tokens.
        currency: Currency symbol (display only).
        precision: Number of decimal places.

    Returns:
        The calculated cost rounded to the requested precision.
    """
    cost = (Decimal(token_count) / Decimal(1000)) * price_per_1000_tokens
    return cost.quantize(Decimal(f"1.{'0' * precision}"))


def format_cost(cost: Decimal, currency: str = "$") -> str:
    """
    Format a Decimal cost for display.

    Args:
        cost: Cost value.
        currency: Currency symbol.

    Returns:
        A formatted string.
    """
    return f"{currency}{cost}"
