from decimal import Decimal

from src.token.cost import calculate_cost, format_cost


def main() -> None:
    """
    Run the token cost example.
    """
    cost = calculate_cost(
        token_count=2500,
        price_per_1000_tokens=Decimal("0.003"),
        currency="$",
        precision=6,
    )

    print(format_cost(cost, currency="$"))


if __name__ == "__main__":
    main()
