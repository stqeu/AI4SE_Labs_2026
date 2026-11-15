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
playground/playground/models.py | method: Money.__bool__
Return True when the amount is non-zero.

Implement this method (it currently has only `pass` as its body):
```python
def __bool__(self) -> bool:
    """Return True when the amount is non-zero."""
```

## Relevant code from the repository
### Context 1 (similarity 0.81)
```python
# file: playground/playground/models.py | method: Money.__init__ | lines 15-21
class Money:
    """Immutable integer-cents amount."""
    def __init__(self, cents: int = 0) -> None:
        # attributes set in __init__:
        self._cents = cents
    ...
    def __init__(self, cents: int = 0) -> None:
        """Create a monetary amount; cents must be a non-negative ``int``."""
        if isinstance(cents, bool) or not isinstance(cents, int):
            raise TypeError("cents must be int")
        if cents < 0:
            raise ValueError("money cannot be negative")
        self._cents = cents
```

### Context 2 (similarity 0.80)
```python
# file: playground/playground/models.py | method: Money.__le__ | lines 72-76
class Money:
    """Immutable integer-cents amount."""
    def __init__(self, cents: int = 0) -> None:
        # attributes set in __init__:
        self._cents = cents
    ...
    def __le__(self, other: Money) -> bool:
        """Return True if ``self`` is less than or equal to ``other``."""
        if not isinstance(other, Money):
            return NotImplemented
        return self._cents <= other._cents
```

### Context 3 (similarity 0.80)
```python
# file: playground/playground/models.py | method: Money.__mul__ | lines 48-54
class Money:
    """Immutable integer-cents amount."""
    def __init__(self, cents: int = 0) -> None:
        # attributes set in __init__:
        self._cents = cents
    ...
    def __mul__(self, factor: int) -> Money:
        """Return ``self`` multiplied by a non-negative integer."""
        if isinstance(factor, bool) or not isinstance(factor, int):
            raise TypeError("factor must be int")
        if factor < 0:
            raise ValueError("factor cannot be negative")
        return Money(self._cents * factor)
```

### Context 4 (similarity 0.80)
```python
# file: playground/playground/models.py | method: Money.__lt__ | lines 66-70
class Money:
    """Immutable integer-cents amount."""
    def __init__(self, cents: int = 0) -> None:
        # attributes set in __init__:
        self._cents = cents
    ...
    def __lt__(self, other: Money) -> bool:
        """Return True if ``self`` is strictly less than ``other``."""
        if not isinstance(other, Money):
            return NotImplemented
        return self._cents < other._cents
```

### Context 5 (similarity 0.79)
```python
# file: playground/playground/models.py | method: Money.__eq__ | lines 60-64
class Money:
    """Immutable integer-cents amount."""
    def __init__(self, cents: int = 0) -> None:
        # attributes set in __init__:
        self._cents = cents
    ...
    def __eq__(self, other: object) -> bool:
        """Return True if ``other`` is Money with equal cents."""
        if not isinstance(other, Money):
            return NotImplemented
        return self._cents == other._cents
```

Return only the complete method definition with the docstring, in one ```python block.
