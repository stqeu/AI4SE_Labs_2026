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
playground/playground/orders.py | method: OrderLog.by_status
Yield orders whose status matches ``status``.

Implement this method (it currently has only `pass` as its body):
```python
def by_status(self, status: OrderStatus) -> Iterator[Order]:
    """Yield orders whose status matches ``status``."""
```

## Relevant code from the repository
### Context 1 (similarity 0.81)
```python
# file: playground/playground/orders.py | method: Order.status | lines 71-74
class Order:
    """Customer order with items, status, and pricing."""
    def __init__(self, order_id: str, customer: Customer, pricing: PricingStrategy) -> None:
        # attributes set in __init__:
        self._order_id = order_id
        self._customer = customer
        self._pricing = pricing
        self._items: List[LineItem] = []
        self._status: OrderStatus = OrderStatus.NEW
        self._machine = OrderStateMachine()
    ...
    @property
    def status(self) -> OrderStatus:
        """Return the current order status."""
        return self._status
```

### Context 2 (similarity 0.73)
```python
# file: playground/playground/orders.py | method: OrderLog.__iter__ | lines 194-196
class OrderLog:
    """Ordered, deduplicated record of orders; iterable."""
    def __init__(self) -> None:
        # attributes set in __init__:
        self._orders: List[Order] = []
    ...
    def __iter__(self) -> Iterator[Order]:
        """Iterate over the logged orders."""
        yield from list(self._orders)
```

### Context 3 (similarity 0.73)
```python
# file: playground/playground/orders.py | method: OrderLog.__getitem__ | lines 186-188
class OrderLog:
    """Ordered, deduplicated record of orders; iterable."""
    def __init__(self) -> None:
        # attributes set in __init__:
        self._orders: List[Order] = []
    ...
    def __getitem__(self, index: int) -> Order:
        """Return the order at ``index``."""
        return self._orders[index]
```

### Context 4 (similarity 0.72)
```python
# file: playground/playground/orders.py | method: OrderLog.__init__ | lines 170-172
class OrderLog:
    """Ordered, deduplicated record of orders; iterable."""
    def __init__(self) -> None:
        # attributes set in __init__:
        self._orders: List[Order] = []
    ...
    def __init__(self) -> None:
        """Create an empty order log."""
        self._orders: List[Order] = []
```

### Context 5 (similarity 0.71)
```python
# file: playground/playground/orders.py | class_skeleton: OrderLog | lines 167-196
class OrderLog:
    """Ordered, deduplicated record of orders; iterable."""
    def __init__(self) -> None:
        """Create an empty order log."""
        ...
    def record(self, order: Order) -> None:
        """Append ``order``; raises if an order with the same id is already logged."""
        ...
    def by_status(self, status: OrderStatus) -> Iterator[Order]:
        ...  # NOT IMPLEMENTED
    def __getitem__(self, index: int) -> Order:
        """Return the order at ``index``."""
        ...
    def __len__(self) -> int:
        """Return the number of logged orders."""
        ...
    def __iter__(self) -> Iterator[Order]:
        """Iterate over the logged orders."""
        ...
```

Return only the complete method definition with the docstring, in one ```python block.
