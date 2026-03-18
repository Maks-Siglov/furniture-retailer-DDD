from src.models import Batch, OrderLine


def test_allocate_reduce_batch_quantity():
    batch = Batch(reference="sdg-243", quantity=10, sku="BLUE-VASE")
    line = OrderLine(order_id="order-143", quantity=4, sku="BLUE-VASE")

    desired_quantity = batch.available_quantity - line.quantity

    batch.allocate(line)

    assert batch.available_quantity == desired_quantity


def test_can_allocate_batch_and_line():
    batch = Batch(reference="sdg-243", quantity=10, sku="BLUE-VASE")
    line = OrderLine(order_id="order-143", quantity=4, sku="BLUE-VASE")

    assert batch.can_allocate(line)


def test_can_allocate_batch_and_line_when_qty_is_equal():
    qty = 10
    batch = Batch(reference="sdg-243", quantity=qty, sku="BLUE-VASE")
    line = OrderLine(order_id="order-143", quantity=qty, sku="BLUE-VASE")

    assert batch.can_allocate(line)


def test_cannot_allocate_larger_order_line():
    batch = Batch(reference="sf-255", quantity=10, sku="BLUE-VASE")
    line = OrderLine(order_id="order-125", quantity=12, sku="BLUE-VASE")

    assert batch.can_allocate(line) is False


def test_cannot_allocate_different_sku_to_batch():
    batch = Batch(reference="sf-255", quantity=10, sku="BLUE-VASE")
    different_sku_line = OrderLine(
        order_id="order-125", quantity=2, sku="RED-CHAIR"
    )

    assert batch.can_allocate(different_sku_line) is False


def test_batch_allocation_idempotent():
    batch = Batch(reference="rf-326", quantity=10, sku="BLUE-VASE")
    line = OrderLine(order_id="order-272", quantity=2, sku="BLUE-VASE")

    desired_quantity = batch.available_quantity - line.quantity

    batch.allocate(line)
    batch.allocate(line)

    assert batch.available_quantity == desired_quantity


def test_batch_deallocate_line():
    initial_qty = 10
    batch = Batch(reference="rf-326", quantity=initial_qty, sku="BLUE-VASE")
    line = OrderLine(order_id="order-272", quantity=2, sku="BLUE-VASE")

    batch.allocate(line)
    batch.deallocate(line)

    assert batch.available_quantity == initial_qty


def can_deallocate_only_allocated_lines():
    batch = Batch(reference="rf-326", quantity=10, sku="BLUE-VASE")
    allocated_line = OrderLine(
        order_id="order-272", quantity=2, sku="BLUE-VASE"
    )

    not_allocated_line = OrderLine(
        order_id="order-272", quantity=2, sku="BLUE-VASE"
    )

    desired_quantity = batch.available_quantity - allocated_line.quantity

    batch.allocate(allocated_line)
    batch.deallocate(not_allocated_line)

    assert batch.available_quantity == desired_quantity
