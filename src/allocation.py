from src.exceptions import OutOfStock
from src.models import Batch, OrderLine


def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(
            batch for batch in sorted(batches) if batch.can_allocate(line)
        )
    except StopIteration:
        raise OutOfStock(f"Cannot allocate {line} with {len(batches)} batches")

    batch.allocate(line)
    return batch.reference
