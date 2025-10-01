from dintero.error import InvalidFieldError


def validate_session(session):
    """
    Validates that the session's total order amount matches the sum of the
    item amounts plus the shipping amount.
    """
    order = session.get("order", {})
    items_total = sum(item.get("amount", 0) for item in order.get("items", []))
    shipping_amount = order.get("shipping_option", {}).get("amount", 0)

    if order.get("amount") != items_total + shipping_amount:
        raise InvalidFieldError(
            "order.amount does not match the sum of order.items and shipping_option.amount",
            "order.amount",
        )
