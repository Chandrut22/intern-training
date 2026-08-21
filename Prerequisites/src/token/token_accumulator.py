from decimal import Decimal

from src.token import calculate_cost, format_cost


class TokenAccumulator:
    """Accumulate token counts across many add() calls and report running cost."""

    def __init__(
        self,
        price_per_1000_tokens: Decimal = Decimal("0.002"),
        currency: str = "$",
    ) -> None:
        self._total_tokens = 0
        self._price_per_1000_tokens = price_per_1000_tokens
        self._currency = currency

    def add(self, token_count: int) -> Decimal:
        """Add token_count to the running total and return the new running cost."""
        self._total_tokens += token_count
        return self.running_cost()

    @property
    def total_tokens(self) -> int:
        return self._total_tokens

    def running_cost(self) -> Decimal:
        """Current accumulated cost for all tokens seen so far."""
        return calculate_cost(
            token_count=self._total_tokens,
            price_per_1000_tokens=self._price_per_1000_tokens,
        )

    def report(self) -> str:
        return format_cost(self.running_cost(), currency=self._currency)
