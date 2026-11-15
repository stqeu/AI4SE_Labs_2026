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
playground/playground/models.py | method: Customer.can_afford
Return True if ``balance + total`` does not exceed the credit limit.

Implement this method (it currently has only `pass` as its body):
```python
def can_afford(self, total: Money) -> bool:
    """Return True if ``balance + total`` does not exceed the credit limit."""
```

## Relevant code from the repository
### Context 1 (similarity 0.80)
```python
# file: playground/playground/models.py | method: Customer.charge | lines 264-268
class Customer(Entity):
    """Buyer with a credit limit. Balance is the amount owed."""
    def __init__(self, customer_id: str, name: str, credit_limit: Money = Money(0)) -> None:
        # attributes set in __init__:
        self._customer_id = customer_id
        self._name = name
        self._credit_limit = credit_limit
        self._balance = Money(0)
    ...
    def charge(self, total: Money) -> None:
        """Increase the balance by ``total``, raising if the limit would be exceeded."""
        if not self.can_afford(total):
            raise ValueError("credit limit exceeded")
        self._balance = self._balance + total
```

### Context 2 (similarity 0.77)
```python
# file: playground/playground/models.py | method: Customer.credit_limit | lines 247-250
class Customer(Entity):
    """Buyer with a credit limit. Balance is the amount owed."""
    def __init__(self, customer_id: str, name: str, credit_limit: Money = Money(0)) -> None:
        # attributes set in __init__:
        self._customer_id = customer_id
        self._name = name
        self._credit_limit = credit_limit
        self._balance = Money(0)
    ...
    @property
    def credit_limit(self) -> Money:
        """Return the credit limit."""
        return self._credit_limit
```

### Context 3 (similarity 0.71)
```python
# file: playground/tests/test_models.py | test: CustomerTests.test_can_afford_false_over_limit | lines 453-455
class CustomerTests(unittest.TestCase):
    ...
    def test_can_afford_false_over_limit(self) -> None:
        c = Customer("C-1", "A", Money(1000))
        self.assertFalse(c.can_afford(Money(1001)))
```

### Context 4 (similarity 0.70)
```python
# file: playground/tests/test_models.py | test: CustomerTests.test_can_afford_accounts_for_existing_balance | lines 457-461
class CustomerTests(unittest.TestCase):
    ...
    def test_can_afford_accounts_for_existing_balance(self) -> None:
        c = Customer("C-1", "A", Money(1000))
        c.charge(Money(600))
        self.assertTrue(c.can_afford(Money(400)))
        self.assertFalse(c.can_afford(Money(401)))
```

### Context 5 (similarity 0.70)
```python
# file: playground/tests/test_models.py | test: CustomerTests.test_can_afford_true_within_limit | lines 449-451
class CustomerTests(unittest.TestCase):
    ...
    def test_can_afford_true_within_limit(self) -> None:
        c = Customer("C-1", "A", Money(1000))
        self.assertTrue(c.can_afford(Money(1000)))
```

Return only the complete method definition with the docstring, in one ```python block.
