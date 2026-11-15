# SYSTEM
You are an expert Python developer working in an existing code base.
You implement exactly ONE missing method.
Rules:
- Return ONLY the complete method definition: the `def` line, the given docstring and the body.
- Do not return the class, imports, decorators, tests or any explanation.
- Keep the exact signature that is given.
- Use only names that exist in the code base or the standard library (see the context).
- Answer with a single ```python code block.

# USER
## Task
playground/playground/inventory.py | method: Warehouse.stock_report
Return a mapping of SKU to available quantity.

Implement this method (it currently has only `pass` as its body):
```python
def stock_report(self) -> Dict[str, int]:
    """Return a mapping of SKU to available quantity."""
```

## Relevant code from the repository
### Context 1 (similarity 0.75)
```python
# file: playground/playground/inventory.py | method: Warehouse.receive | lines 146-148
class Warehouse(Entity):
    """Named location owning an :class:`InventoryLedger`."""
    def __init__(self, warehouse_id: str, name: str, ledger: InventoryLedger) -> None:
        # attributes set in __init__:
        self._warehouse_id = warehouse_id
        self._name = name
        self._ledger = ledger
    ...
    def receive(self, sku: str, quantity: int) -> int:
        """Add stock to the warehouse ledger; return the new on-hand total."""
        return self._ledger.add_stock(sku, quantity)
```

### Context 2 (similarity 0.70)
```python
# file: playground/playground/inventory.py | module: inventory | lines 1-9
"""Inventory ledger and warehouse location."""
from __future__ import annotations
from typing import Dict, Iterator
from .base import Entity, Repository
from .exceptions import InvalidTransitionError, OutOfStockError, UnknownSKUError
from .util import ensure_positive_int, normalize_sku
```

### Context 3 (similarity 0.69)
```python
# file: playground/playground/inventory.py | method: InventoryLedger.available | lines 37-40
class InventoryLedger:
    """Tracks on-hand and reserved quantities per SKU."""
    def __init__(self, product_repo: Repository) -> None:
        # attributes set in __init__:
        self._product_repo = product_repo
        self._on_hand: Dict[str, int] = {}
        self._reserved: Dict[str, int] = {}
    ...
    def available(self, sku: str) -> int:
        """Return on-hand minus reserved for ``sku``."""
        sku = self._require_sku(sku)
        return self._on_hand.get(sku, 0) - self._reserved.get(sku, 0)
```

### Context 4 (similarity 0.68)
```python
# file: playground/playground/inventory.py | method: InventoryLedger.add_stock | lines 30-35
class InventoryLedger:
    """Tracks on-hand and reserved quantities per SKU."""
    def __init__(self, product_repo: Repository) -> None:
        # attributes set in __init__:
        self._product_repo = product_repo
        self._on_hand: Dict[str, int] = {}
        self._reserved: Dict[str, int] = {}
    ...
    def add_stock(self, sku: str, quantity: int) -> int:
        """Add ``quantity`` to on-hand stock for ``sku``; return the new total."""
        quantity = ensure_positive_int(quantity, "quantity")
        sku = self._require_sku(sku)
        self._on_hand[sku] = self._on_hand.get(sku, 0) + quantity
        return self._on_hand[sku]
```

### Context 5 (similarity 0.67)
```python
# file: playground/playground/inventory.py | class_skeleton: Warehouse | lines 124-155
class Warehouse(Entity):
    """Named location owning an :class:`InventoryLedger`."""
    def __init__(self, warehouse_id: str, name: str, ledger: InventoryLedger) -> None:
        """Create a warehouse with the given id, name, and ledger."""
        ...
    def identity(self) -> str:
        """Return the warehouse_id as the entity identity."""
        ...
    @property
    def ledger(self) -> InventoryLedger:
        """Return the warehouse inventory ledger."""
        ...
    def receive(self, sku: str, quantity: int) -> int:
        """Add stock to the warehouse ledger; return the new on-hand total."""
        ...
    def stock_report(self) -> Dict[str, int]:
        ...  # NOT IMPLEMENTED
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        ...
```

Return only the complete method definition with the docstring, in one ```python block.
