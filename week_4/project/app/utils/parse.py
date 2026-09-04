from typing import Any


def parse_comma_separated_list(v: Any) -> list[str]:
    """
    Parse a comma-separated string into a list of trimmed, non-empty strings.
    Strips surrounding quotes so values like 'a,b' or "a,b" both work.
    """
    if isinstance(v, str):
        v = v.strip("'\" ")
        return [item.strip() for item in v.split(",") if item.strip()]
    return v
