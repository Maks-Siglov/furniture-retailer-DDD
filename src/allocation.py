from src.models import Batch, OrderLine


def allocate(line: OrderLine, batches: list[Batch]) -> str:
    batch = next(
        batch for batch in sorted(batches) if batch.can_allocate(line)
    )

    batch.allocate(line)
    return batch.reference
