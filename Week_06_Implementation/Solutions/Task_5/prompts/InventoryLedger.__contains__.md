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
playground/playground/inventory.py | method: InventoryLedger.__contains__
Return whether ``sku`` normalises to a SKU with positive on-hand stock.

Implement this method (it currently has only `pass` as its body):
```python
def __contains__(self, sku: object) -> bool:
    """Return whether ``sku`` normalises to a SKU with positive on-hand stock."""
```

## Relevant code from the repository
### Context 1 (similarity 0.77)
```python
# file: playground/playground/inventory.py | method: InventoryLedger.__len__ | lines 74-76
class InventoryLedger:
    """Tracks on-hand and reserved quantities per SKU."""
    def __init__(self, product_repo: Repository) -> None:
        # attributes set in __init__:
        self._product_repo = product_repo
        self._on_hand: Dict[str, int] = {}
        self._reserved: Dict[str, int] = {}
    ...
    def __len__(self) -> int:
        """Return the number of SKUs with positive on-hand stock."""
        return sum(1 for qty in self._on_hand.values() if qty > 0)
```

### Context 2 (similarity 0.77)
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

### Context 3 (similarity 0.76)
```python
# file: playground/playground/inventory.py | method: InventoryLedger.__iter__ | lines 78-81
class InventoryLedger:
    """Tracks on-hand and reserved quantities per SKU."""
    def __init__(self, product_repo: Repository) -> None:
        # attributes set in __init__:
        self._product_repo = product_repo
        self._on_hand: Dict[str, int] = {}
        self._reserved: Dict[str, int] = {}
    ...
    def __iter__(self) -> Iterator[str]:
        """Iterate over SKUs with positive on-hand stock, in sorted order."""
        for sku in sorted(k for k, v in self._on_hand.items() if v > 0):
            yield sku
```

### Context 4 (similarity 0.76)
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

### Context 5 (similarity 0.75)
```python
# file: playground/playground/inventory.py | method: InventoryLedger._require_sku | lines 23-28
class InventoryLedger:
    """Tracks on-hand and reserved quantities per SKU."""
    def __init__(self, product_repo: Repository) -> None:
        # attributes set in __init__:
        self._product_repo = product_repo
        self._on_hand: Dict[str, int] = {}
        self._reserved: Dict[str, int] = {}
    ...
    def _require_sku(self, sku: str) -> str:
        """Normalise ``sku`` and raise ``UnknownSKUError`` if it is unregistered."""
        sku = normalize_sku(sku)
        if sku not in self._product_repo:
            raise UnknownSKUError(sku)
        return sku
```

Return only the complete method definition with the docstring, in one ```python block.
