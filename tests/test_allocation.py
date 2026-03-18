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


# from ... import AllocationService
#
#
# def test_allocation_prefers_warehouse_over_shipment():
#     line = OrderLine(order_id="order-272",quantity=4, sku="BLUE-VASE")
#
#     batch_in_stock = Batch(reference="ref-2634",quantity=10, sku="BLUE-VASE")
#     batch_in_shipment = Batch(
#         reference="ref-2536",
#         quantity=10,
#         sku="BLUE-VASE",
#         eta=datetime.date(year=2026, month=6, day=17),
#     )
#
#     allocation_service = AllocationService()
#     allocation_service.add_batch(batch_in_stock)
#     allocation_service.add_batch(batch_in_shipment)
#
#     batch_to_allocate = allocation_service.pick_batch(line)
#     assert batch_to_allocate == batch_in_stock
#
#
# def test_allocation_prefers_earliest_eta_batch():
#     line = OrderLine(order_id="order-272",quantity=4, sku="BLUE-TABLE")
#
#     # Will be in stock first
#     batch_in_shipment1 = Batch(
#         reference="ref-236",
#         quantity=10,
#         sku="BLUE-TABLE",
#         eta=datetime.date(year=2026, month=6, day=16),
#     )
#     # Will be in stock second
#     batch_in_shipment2 = Batch(
#         reference="ref-782",
#         quantity=10,
#         sku="BLUE-TABLE",
#         eta=datetime.date(year=2026, month=6, day=17),
#     )
#
#     allocation_service = AllocationService()
#     allocation_service.add_batch(batch_in_shipment1)
#     allocation_service.add_batch(batch_in_shipment2)
#
#     batch_to_allocate = allocation_service.pick_batch(line)
#     assert batch_to_allocate == batch_in_shipment1
