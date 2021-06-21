from dintero.error import InvalidFieldError


def validate_session(session):
    if session["order"]["amount"] != sum(
        [item["amount"] for item in session["order"]["items"]]
    ):
        raise InvalidFieldError(
            "order.amount doesn't match sum of order.items", "order.amount"
        )
