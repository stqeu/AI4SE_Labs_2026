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
playground/playground/pricing.py | method: BulkDiscountPricing.price
Return the base price, less the discount if the quantity qualifies.

Implement this method (it currently has only `pass` as its body):
```python
def price(self, items: Sequence[LineItem]) -> Money:
    """Return the base price, less the discount if the quantity qualifies."""
```

## Relevant code from the repository
### Context 1 (similarity 0.80)
```python
# file: playground/playground/pricing.py | method: BulkDiscountPricing.threshold | lines 53-56
class BulkDiscountPricing(PricingStrategy):
    """Wraps another strategy; applies a percent discount when total quantity meets a threshold."""
    def __init__(self, base: PricingStrategy, threshold: int, percent_off: int) -> None:
        # attributes set in __init__:
        self._base = base
        self._threshold = threshold
        self._percent_off = percent_off
    ...
    @property
    def threshold(self) -> int:
        """Return the qualifying total quantity."""
        return self._threshold
```

### Context 2 (similarity 0.80)
```python
# file: playground/playground/pricing.py | method: BulkDiscountPricing.percent_off | lines 58-61
class BulkDiscountPricing(PricingStrategy):
    """Wraps another strategy; applies a percent discount when total quantity meets a threshold."""
    def __init__(self, base: PricingStrategy, threshold: int, percent_off: int) -> None:
        # attributes set in __init__:
        self._base = base
        self._threshold = threshold
        self._percent_off = percent_off
    ...
    @property
    def percent_off(self) -> int:
        """Return the discount percentage."""
        return self._percent_off
```

### Context 3 (similarity 0.79)
```python
# file: playground/playground/pricing.py | method: BulkDiscountPricing.__repr__ | lines 66-68
class BulkDiscountPricing(PricingStrategy):
    """Wraps another strategy; applies a percent discount when total quantity meets a threshold."""
    def __init__(self, base: PricingStrategy, threshold: int, percent_off: int) -> None:
        # attributes set in __init__:
        self._base = base
        self._threshold = threshold
        self._percent_off = percent_off
    ...
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"BulkDiscountPricing(threshold={self._threshold}, percent_off={self._percent_off})"
```

### Context 4 (similarity 0.75)
```python
# file: playground/playground/pricing.py | class_skeleton: BulkDiscountPricing | lines 37-68
class BulkDiscountPricing(PricingStrategy):
    """Wraps another strategy; applies a percent discount when total quantity meets a threshold."""
    def __init__(self, base: PricingStrategy, threshold: int, percent_off: int) -> None:
        """Create a strategy that discounts ``base`` totals above ``threshold`` quantity."""
        ...
    @property
    def threshold(self) -> int:
        """Return the qualifying total quantity."""
        ...
    @property
    def percent_off(self) -> int:
        """Return the discount percentage."""
        ...
    def price(self, items: Sequence[LineItem]) -> Money:
        ...  # NOT IMPLEMENTED
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        ...
```

### Context 5 (similarity 0.75)
```python
# file: playground/tests/test_pricing.py | test: BulkDiscountPriceTests.test_below_threshold_returns_base_total | lines 119-122
class BulkDiscountPriceTests(unittest.TestCase):
    ...
    def test_below_threshold_returns_base_total(self) -> None:
        items = [LineItem("EL-1001", 2, Money(1000))]
        d = BulkDiscountPricing(FlatPricing(), 3, 50)
        self.assertEqual(d.price(items), Money(2000))
```

Return only the complete method definition with the docstring, in one ```python block.
