import pytest

from dintero.error import InvalidFieldError
from dintero.validator import validate_session


def test_validate_session_valid():
    """
    Should not raise an exception when the order amount matches the sum of
    the item amounts.
    """
    session = {
        "order": {
            "amount": 60000,
            "items": [
                {"amount": 10000},
                {"amount": 20000},
                {"amount": 30000},
            ],
        }
    }
    validate_session(session)


def test_validate_session_shipping_option_valid():
    """
    Should not raise an exception when the order amount matches the sum of
    the item amounts and shipping option.
    """
    session = {
        "order": {
            "amount": 70000,
            "items": [
                {"amount": 10000},
                {"amount": 20000},
                {"amount": 30000},
            ],
            "shipping_option": {
                "amount": 10000,
            },
        },
    }
    validate_session(session)


def test_validate_session_invalid_raises_error():
    """
    Should raise InvalidFieldError when the order amount does not match the
    sum of the item amounts.
    """
    session = {
        "order": {
            "amount": 50000,
            "items": [
                {"amount": 10000},
                {"amount": 20000},
                {"amount": 30000},
            ],
        }
    }
    with pytest.raises(InvalidFieldError) as excinfo:
        validate_session(session)
    assert (
        "order.amount does not match the sum of order.items and shipping_option.amount"
        in str(excinfo.value)
    )
    assert excinfo.value.field == "order.amount"
