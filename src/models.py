import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int


class Batch:
    def __init__(
        self,
        reference: str,
        sku: str,
        quantity: int,
        eta: datetime.date | None = None,
    ):
        self.reference = reference
        self.sku = sku
        self.available_quantity = quantity
        self.eta = eta

    def allocate(self, line: OrderLine):
        self.available_quantity -= line.quantity
