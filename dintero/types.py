from typing_extensions import TypedDict


class Item(TypedDict):
    amount: int
    line_id: str
    id: str
    description: str
    quantity: int
    vat_amount: int
    vat: int
