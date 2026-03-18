import datetime

import pytest

from ... import AllocationService, Batch, OrderLine


def test_allocate_reduce_batch_quantity():
    batch = Batch(quantity=10, sku="BLUE-VASE")
    line = OrderLine(quantity=4, sku="BLUE-VASE")

    desired_quantity = batch.quantity - line.quantity

    batch.allocate(line)

    assert batch.quantity == desired_quantity


def test_cannot_allocate_larger_order_line():
    batch = Batch(quantity=10, sku="BLUE-VASE")
    line = OrderLine(quantity=12, sku="BLUE-VASE")

    with pytest.raises(ValueError):
        batch.allocate(line)


def test_cannot_allocate_different_sku_to_batch():
    batch = Batch(quantity=10, sku="BLUE-VASE")
    line = OrderLine(quantity=2, sku="RED-CHAIR")

    with pytest.raises(ValueError):
        batch.allocate(line)


def test_batch_allocation_idempotent():
    batch = Batch(quantity=10, sku="BLUE-VASE")
    line = OrderLine(quantity=2, sku="BLUE-VASE")

    desired_quantity = batch.quantity - line.quantity

    batch.allocate(line)
    batch.allocate(line)

    assert batch.quantity == desired_quantity


def test_allocation_prefers_warehouse_over_shipment():
    line = OrderLine(quantity=4, sku="BLUE-VASE")

    batch_in_stock = Batch(quantity=10, sku="BLUE-VASE")
    batch_in_shipment = Batch(
        quantity=10,
        sku="BLUE-VASE",
        eta=datetime.datetime(year=2026, month=6, day=17),
    )

    allocation_service = AllocationService()
    allocation_service.add_batch(batch_in_stock)
    allocation_service.add_batch(batch_in_shipment)

    batch_to_allocate = allocation_service.pick_batch(line)
    assert batch_to_allocate == batch_in_stock


def test_allocation_prefers_earliest_eta_batch():
    line = OrderLine(quantity=4, sku="BLUE-TABLE")

    # Will be in stock first
    batch_in_shipment1 = Batch(
        quantity=10,
        sku="BLUE-TABLE",
        eta=datetime.datetime(year=2026, month=6, day=16),
    )
    # Will be in stock second
    batch_in_shipment2 = Batch(
        quantity=10,
        sku="BLUE-TABLE",
        eta=datetime.datetime(year=2026, month=6, day=17),
    )

    allocation_service = AllocationService()
    allocation_service.add_batch(batch_in_shipment1)
    allocation_service.add_batch(batch_in_shipment2)

    batch_to_allocate = allocation_service.pick_batch(line)
    assert batch_to_allocate == batch_in_shipment1
