# Furniture Retailer DDD

## Domain Requirements

### Glossary

- **SKU** — Stock Keeping Unit (e.g. `RED-CHAIR`, `TASTELESS-LAMP`)
- **ETA** - Estimated Time of Arrivals

### Orders

Customers place **orders**. An order is identified by an order **reference** and comprises multiple **order lines**, where each line has a **SKU** and a **quantity**.

> Example order:
> - 10 units of `RED-CHAIR`
> - 1 unit of `TASTELESS-LAMP`

### Batches

The purchasing department purchases **batches** of stock from manufacturers. A batch has:

- A unique **reference**
- A **SKU**
- A **quantity**

### Allocation Rules

1. Order lines are allocated to batches. When an order line is allocated to a batch, the batch's available quantity is reduced accordingly.

   > Example: A batch of 18 `SMALL-TABLE` exists. We allocate an order line of 2 `SMALL-TABLE`. The batch now has 16 `SMALL-TABLE` available.

2. An order line **cannot** be allocated to a batch if the available quantity is less than the order line quantity.

3. The same order line **cannot** be allocated twice.

   > Example: A batch of 10 `BLUE-TABLE` exists. We allocate an order line of 2 `BLUE-TABLE`. If we allocate that same order line again to the same batch, the available quantity should still be 8.

4. Batches may have an **ETA** (if currently shipping) or may already be in **warehouse stock**. Allocation preference:
   - Warehouse stock is preferred over shipment batches.
   - Among shipment batches, allocate to the one with the **earliest ETA**.
