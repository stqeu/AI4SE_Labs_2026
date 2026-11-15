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
playground/playground/events.py | method: EventBus.__contains__
Return whether any handlers are registered for ``event_type``.

Implement this method (it currently has only `pass` as its body):
```python
def __contains__(self, event_type: object) -> bool:
    """Return whether any handlers are registered for ``event_type``."""
```

## Relevant code from the repository
### Context 1 (similarity 0.76)
```python
# file: playground/playground/events.py | method: EventBus.__init__ | lines 14-16
class EventBus:
    """Synchronous publish/subscribe keyed by :class:`EventType`."""
    def __init__(self) -> None:
        # attributes set in __init__:
        self._handlers: Dict[EventType, List[Callable[..., None]]] = {}
    ...
    def __init__(self) -> None:
        """Initialise an empty handler registry."""
        self._handlers: Dict[EventType, List[Callable[..., None]]] = {}
```

### Context 2 (similarity 0.69)
```python
# file: playground/playground/events.py | method: EventBus.subscribe | lines 18-24
class EventBus:
    """Synchronous publish/subscribe keyed by :class:`EventType`."""
    def __init__(self) -> None:
        # attributes set in __init__:
        self._handlers: Dict[EventType, List[Callable[..., None]]] = {}
    ...
    def subscribe(self, event_type: EventType, handler: Callable[..., None]) -> None:
        """Register ``handler`` to be called when ``event_type`` is published."""
        if not isinstance(event_type, EventType):
            raise TypeError("event_type must be EventType")
        if not callable(handler):
            raise TypeError("handler must be callable")
        self._handlers.setdefault(event_type, []).append(handler)
```

### Context 3 (similarity 0.69)
```python
# file: playground/playground/events.py | method: EventBus.__len__ | lines 49-51
class EventBus:
    """Synchronous publish/subscribe keyed by :class:`EventType`."""
    def __init__(self) -> None:
        # attributes set in __init__:
        self._handlers: Dict[EventType, List[Callable[..., None]]] = {}
    ...
    def __len__(self) -> int:
        """Return the total number of registered handlers across all event types."""
        return sum(len(handlers) for handlers in self._handlers.values())
```

### Context 4 (similarity 0.68)
```python
# file: playground/playground/events.py | method: EventBus.unsubscribe | lines 26-32
class EventBus:
    """Synchronous publish/subscribe keyed by :class:`EventType`."""
    def __init__(self) -> None:
        # attributes set in __init__:
        self._handlers: Dict[EventType, List[Callable[..., None]]] = {}
    ...
    def unsubscribe(self, event_type: EventType, handler: Callable[..., None]) -> bool:
        """Remove ``handler`` from ``event_type``; return whether it was present."""
        handlers = self._handlers.get(event_type, [])
        if handler not in handlers:
            return False
        handlers.remove(handler)
        return True
```

### Context 5 (similarity 0.66)
```python
# file: playground/tests/test_events.py | test: EventBusContainsTests.test_contains_false_without_handlers | lines 153-154
class EventBusContainsTests(unittest.TestCase):
    ...
    def test_contains_false_without_handlers(self) -> None:
        self.assertNotIn(EventType.ORDER_SHIPPED, EventBus())
```

Return only the complete method definition with the docstring, in one ```python block.
