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
playground/playground/enums.py | method: OrderStatus.is_terminal
True when the status ends further transitions.

Implement this method (it currently has only `pass` as its body):
```python
@property
def is_terminal(self) -> bool:
    """True when the status ends further transitions."""
```

## Relevant code from the repository
### Context 1 (similarity 0.77)
```python
# file: playground/playground/enums.py | class_skeleton: OrderStatus | lines 37-47
class OrderStatus(Enum):
    """Lifecycle stages for an order."""
    NEW = "new"
    RESERVED = "reserved"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"
    @property
    def is_terminal(self) -> bool:
        ...  # NOT IMPLEMENTED
```

### Context 2 (similarity 0.68)
```python
# file: playground/tests/test_enums.py | test: OrderStatusTests.test_cancelled_is_terminal | lines 60-61
class OrderStatusTests(unittest.TestCase):
    ...
    def test_cancelled_is_terminal(self) -> None:
        self.assertIs(OrderStatus.CANCELLED.is_terminal, True)
```

### Context 3 (similarity 0.67)
```python
# file: playground/tests/test_enums.py | test: OrderStatusTests.test_new_is_not_terminal | lines 63-64
class OrderStatusTests(unittest.TestCase):
    ...
    def test_new_is_not_terminal(self) -> None:
        self.assertIs(OrderStatus.NEW.is_terminal, False)
```

### Context 4 (similarity 0.64)
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

### Context 5 (similarity 0.63)
```python
# file: playground/tests/test_enums.py | test: OrderStatusTests.test_shipped_is_terminal | lines 57-58
class OrderStatusTests(unittest.TestCase):
    ...
    def test_shipped_is_terminal(self) -> None:
        self.assertIs(OrderStatus.SHIPPED.is_terminal, True)
```

Return only the complete method definition with the docstring, in one ```python block.
