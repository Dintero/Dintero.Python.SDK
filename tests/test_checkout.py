from dintero.checkout import Checkout
import pytest

from dintero.error import InvalidFieldError


class TestDinteroCheckout(object):
    def test_item_amounts_match(self):
        localhost_ = "https://localhost:8080"
        checkout = Checkout(
            localhost_,
            localhost_,
            "T12345678",
            "mock_client_id",
            "mock_client_secret",
            "test",
            "0.0.0",
        )
        with pytest.raises(InvalidFieldError) as err:
            checkout.create_session(
                {"order": {"amount": 10, "items": [{"amount": 5}]}}
            )
        assert err.value.field == "order.amount"
