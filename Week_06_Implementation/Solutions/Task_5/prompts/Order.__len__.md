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
playground/playground/orders.py | method: Order.__len__
Return the number of line items.

Implement this method (it currently has only `pass` as its body):
```python
def __len__(self) -> int:
    """Return the number of line items."""
```

## Relevant code from the repository
### Context 1 (similarity 0.87)
```python
# file: playground/playground/orders.py | method: OrderBuilder.__len__ | lines 158-160
class OrderBuilder:
    """Fluent construction of an :class:`Order`."""
    def __init__(self, customer: Customer, pricing: PricingStrategy) -> None:
        # attributes set in __init__:
        self._customer = customer
        self._pricing = pricing
        self._lines: List[Tuple[str, int, Money]] = []
    ...
    def __len__(self) -> int:
        """Return the number of recorded lines."""
        return len(self._lines)
```

### Context 2 (similarity 0.75)
```python
# file: playground/playground/orders.py | method: Order.items | lines 76-79
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
    def items(self) -> Tuple[LineItem, ...]:
        """Return a tuple copy of the order's line items."""
        return tuple(self._items)
```

### Context 3 (similarity 0.75)
```python
# file: playground/playground/orders.py | method: Order.__iter__ | lines 106-108
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
    def __iter__(self) -> Iterator[LineItem]:
        """Iterate over a tuple snapshot of the order's line items."""
        return iter(tuple(self._items))
```

### Context 4 (similarity 0.75)
```python
# file: playground/playground/orders.py | method: OrderLog.__len__ | lines 190-192
class OrderLog:
    """Ordered, deduplicated record of orders; iterable."""
    def __init__(self) -> None:
        # attributes set in __init__:
        self._orders: List[Order] = []
    ...
    def __len__(self) -> int:
        """Return the number of logged orders."""
        return len(self._orders)
```

### Context 5 (similarity 0.68)
```python
# file: playground/playground/orders.py | method: OrderBuilder.__bool__ | lines 162-164
class OrderBuilder:
    """Fluent construction of an :class:`Order`."""
    def __init__(self, customer: Customer, pricing: PricingStrategy) -> None:
        # attributes set in __init__:
        self._customer = customer
        self._pricing = pricing
        self._lines: List[Tuple[str, int, Money]] = []
    ...
    def __bool__(self) -> bool:
        """Return True when at least one line has been recorded."""
        return len(self) > 0
```

Return only the complete method definition with the docstring, in one ```python block.
