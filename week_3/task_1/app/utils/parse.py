
def parse_comma_separated_list(v: any) -> list[str]:
    if isinstance(v, str):
        return [item.strip() for item in v.split(",") if item.strip()]
    return v