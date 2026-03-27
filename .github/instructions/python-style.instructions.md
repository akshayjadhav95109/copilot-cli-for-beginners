# Python Style Guide Instructions

These instructions enforce PEP 8 and modern Python conventions for code quality and consistency.

## Type Hints

All functions and methods must include type hints for parameters and return values:

```python
# ✅ Good
def calculate_total(items: list[float], tax_rate: float) -> float:
    """Calculate total with tax."""
    return sum(items) * (1 + tax_rate)

# ❌ Bad
def calculate_total(items, tax_rate):
    return sum(items) * (1 + tax_rate)
```

Use `typing` module for complex types:

```python
from typing import Optional, Union, TypeVar

T = TypeVar('T')

def find_item(items: list[dict], key: str) -> Optional[dict]:
    """Find item in list by key, return None if not found."""
    return next((item for item in items if key in item), None)

def parse_value(value: Union[int, str, float]) -> str:
    """Parse value to string representation."""
    return str(value)
```

## Naming Conventions

- **Variables/Functions**: Use `snake_case`
- **Classes**: Use `PascalCase`
- **Constants**: Use `UPPER_SNAKE_CASE`
- **Private members**: Prefix with underscore `_private_method`

```python
# ✅ Good
MAX_RETRIES = 3

class DataProcessor:
    def __init__(self):
        self._cache = {}
    
    def process_data(self, raw_data: str) -> dict:
        pass

# ❌ Bad
maxRetries = 3

class dataProcessor:
    def __init__(self):
        self.cache = {}
    
    def processData(self, rawData):
        pass
```

## Code Organization

1. **Imports**: Group and sort (builtins, third-party, local)
2. **Constants**: Define at module level before classes/functions
3. **Classes**: Group related methods together
4. **Functions**: Place public functions before private ones

```python
# ✅ Good import order
import json
from typing import Optional
from pathlib import Path

import requests

from myproject.utils import helper
from myproject.models import User
```

## Docstrings

Use Google-style docstrings:

```python
def create_user(name: str, email: str) -> dict:
    """Create a new user record.
    
    Args:
        name: The user's full name.
        email: The user's email address.
    
    Returns:
        A dictionary containing the created user data.
    
    Raises:
        ValueError: If email is invalid format.
    """
    if '@' not in email:
        raise ValueError(f"Invalid email: {email}")
    return {"name": name, "email": email}
```

## Line Length & Formatting

- Maximum line length: 100 characters
- Use Black formatter for consistency
- Break long lines with parentheses, not backslashes

```python
# ✅ Good
result = calculate_complex_value(
    param1, param2, param3,
    param4=value4, param5=value5
)

# ❌ Bad
result = calculate_complex_value(param1, param2, param3, param4=value4, param5=value5)
```

## Error Handling

Always catch specific exceptions and provide context:

```python
# ✅ Good
try:
    data = json.loads(raw_data)
except json.JSONDecodeError as e:
    logger.error(f"Failed to parse JSON: {e}")
    raise ValueError(f"Invalid JSON data: {raw_data}") from e

# ❌ Bad
try:
    data = json.loads(raw_data)
except:
    pass
```

## Comments & Clarity

- Only comment why, not what (code should be self-documenting)
- Use meaningful variable names
- Keep functions focused and small (under 50 lines)

```python
# ✅ Good
# Cache results to avoid repeated API calls
user_cache = {}

# ❌ Bad
# Get user
u = {}
```
