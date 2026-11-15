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
playground/playground/orders.py | method: OrderStateMachine.transition
Return ``target`` if the transition is allowed, else raise.

Implement this method (it currently has only `pass` as its body):
```python
def transition(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
    """Return ``target`` if the transition is allowed, else raise."""
```

## Relevant code from the repository
### Context 1 (similarity 0.86)
```python
# file: playground/playground/orders.py | method: OrderStateMachine.can_transition | lines 31-33
class OrderStateMachine:
    """Legal OrderStatus transitions, data-driven via TRANSITIONS."""
    TRANSITIONS: Dict[OrderStatus, FrozenSet[OrderStatus]] = {
        OrderStatus.NEW: frozenset({OrderStatus.RESERVED, OrderStatus.CANCELLED}),
        OrderStatus.RESERVED: frozenset({OrderStatus.SHIPPED, OrderStatus.CANCELLED}),
        OrderStatus.SHIPPED: frozenset(),
        OrderStatus.CANCELLED: frozenset(),
    }
    ...
    def can_transition(self, source: OrderStatus, target: OrderStatus) -> bool:
        """Return whether ``target`` is reachable from ``source``."""
        return target in OrderStateMachine.allowed_from(source)
```

### Context 2 (similarity 0.81)
```python
# file: playground/playground/orders.py | method: Order.advance | lines 98-101
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
    def advance(self, target: OrderStatus) -> None:
        """Transition the order to ``target`` status, raising if not allowed."""
        new_status = self._machine.transition(self._status, target)
        self._status = new_status
```

### Context 3 (similarity 0.78)
```python
# file: playground/playground/orders.py | method: OrderStateMachine.__call__ | lines 38-40
class OrderStateMachine:
    """Legal OrderStatus transitions, data-driven via TRANSITIONS."""
    TRANSITIONS: Dict[OrderStatus, FrozenSet[OrderStatus]] = {
        OrderStatus.NEW: frozenset({OrderStatus.RESERVED, OrderStatus.CANCELLED}),
        OrderStatus.RESERVED: frozenset({OrderStatus.SHIPPED, OrderStatus.CANCELLED}),
        OrderStatus.SHIPPED: frozenset(),
        OrderStatus.CANCELLED: frozenset(),
    }
    ...
    def __call__(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
        """Convenience alias for :meth:`transition`."""
        return self.transition(source, target)
```

### Context 4 (similarity 0.72)
```python
# file: playground/playground/orders.py | class_skeleton: OrderStateMachine | lines 14-40
class OrderStateMachine:
    """Legal OrderStatus transitions, data-driven via TRANSITIONS."""
    TRANSITIONS: Dict[OrderStatus, FrozenSet[OrderStatus]] = {
        OrderStatus.NEW: frozenset({OrderStatus.RESERVED, OrderStatus.CANCELLED}),
        OrderStatus.RESERVED: frozenset({OrderStatus.SHIPPED, OrderStatus.CANCELLED}),
        OrderStatus.SHIPPED: frozenset(),
        OrderStatus.CANCELLED: frozenset(),
    }
    @staticmethod
    def allowed_from(status: OrderStatus) -> FrozenSet[OrderStatus]:
        """Return the set of statuses reachable from ``status``."""
        ...
    def can_transition(self, source: OrderStatus, target: OrderStatus) -> bool:
        """Return whether ``target`` is reachable from ``source``."""
        ...
    def transition(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
        ...  # NOT IMPLEMENTED
    def __call__(self, source: OrderStatus, target: OrderStatus) -> OrderStatus:
        """Convenience alias for :meth:`transition`."""
        ...
```

### Context 5 (similarity 0.71)
```python
# file: playground/playground/orders.py | method: OrderStateMachine.allowed_from | lines 24-29
class OrderStateMachine:
    """Legal OrderStatus transitions, data-driven via TRANSITIONS."""
    TRANSITIONS: Dict[OrderStatus, FrozenSet[OrderStatus]] = {
        OrderStatus.NEW: frozenset({OrderStatus.RESERVED, OrderStatus.CANCELLED}),
        OrderStatus.RESERVED: frozenset({OrderStatus.SHIPPED, OrderStatus.CANCELLED}),
        OrderStatus.SHIPPED: frozenset(),
        OrderStatus.CANCELLED: frozenset(),
    }
    ...
    @staticmethod
    def allowed_from(status: OrderStatus) -> FrozenSet[OrderStatus]:
        """Return the set of statuses reachable from ``status``."""
        if not isinstance(status, OrderStatus):
            raise TypeError("status must be OrderStatus")
        return OrderStateMachine.TRANSITIONS[status]
```

Return only the complete method definition with the docstring, in one ```python block.
