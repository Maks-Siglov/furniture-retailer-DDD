import datetime

from src.allocation import allocate
from src.models import Batch, OrderLine


def test_allocation_prefers_warehouse_over_shipment():
    line = OrderLine(order_id="order-272", quantity=4, sku="BLUE-VASE")

    batch_in_stock = Batch(reference="ref-2634", quantity=10, sku="BLUE-VASE")
    desired_qty = batch_in_stock.available_quantity - line.quantity

    initial_qty = 10
    batch_in_shipment = Batch(
        reference="ref-2536",
        quantity=initial_qty,
        sku="BLUE-VASE",
        eta=datetime.date(year=2026, month=6, day=17),
    )

    allocation = allocate(line, [batch_in_stock, batch_in_shipment])

    assert batch_in_stock.available_quantity == desired_qty
    assert batch_in_stock.allocated_quantity == line.quantity

    assert batch_in_shipment.available_quantity == initial_qty

    assert allocation == batch_in_shipment.reference


def test_allocation_prefers_earliest_eta_batch():
    line = OrderLine(order_id="order-272", quantity=4, sku="BLUE-TABLE")

    # Will be in stock first
    batch_in_shipment1 = Batch(
        reference="ref-236",
        quantity=10,
        sku="BLUE-TABLE",
        eta=datetime.date(year=2026, month=6, day=16),
    )
    desired_quantity = batch_in_shipment1.available_quantity - line.quantity
    # Will be in stock second
    initial_qty = 10
    batch_in_shipment2 = Batch(
        reference="ref-782",
        quantity=initial_qty,
        sku="BLUE-TABLE",
        eta=datetime.date(year=2026, month=6, day=17),
    )

    allocation = allocate(line, [batch_in_shipment1, batch_in_shipment2])

    assert batch_in_shipment1.available_quantity == desired_quantity
    assert batch_in_shipment1.allocated_quantity == line.quantity

    assert batch_in_shipment2.available_quantity == initial_qty

    assert allocation == batch_in_shipment1.reference
