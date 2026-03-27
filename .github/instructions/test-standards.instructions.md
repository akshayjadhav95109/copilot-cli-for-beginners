# Pytest Testing Standards

These instructions define pytest conventions and best practices for test file organization and coverage.

## Test File Organization

- Test files named `test_*.py` or `*_test.py`
- Place tests in `tests/` directory parallel to source
- Mirror source structure in test directory

```
myproject/
├── src/
│   ├── models/
│   │   └── user.py
│   └── utils/
│       └── helpers.py
└── tests/
    ├── models/
    │   └── test_user.py
    └── utils/
        └── test_helpers.py
```

## Test Function Structure

Every test should follow the Arrange-Act-Assert (AAA) pattern:

```python
def test_user_creation_with_valid_data():
    """Test that users are created with valid name and email."""
    # Arrange
    user_data = {"name": "John Doe", "email": "john@example.com"}
    
    # Act
    user = User.create(**user_data)
    
    # Assert
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
```

## Naming Conventions

- Test function names: `test_<what_is_being_tested>_<expected_outcome>`
- Test class names: `Test<ComponentName>`
- Test parameters: descriptive names matching the scenario

```python
# ✅ Good test names
def test_calculate_total_returns_correct_sum_with_tax():
    pass

def test_user_login_raises_error_with_invalid_password():
    pass

class TestDataValidator:
    def test_valid_json_passes_validation(self):
        pass

# ❌ Bad test names
def test_total():
    pass

def test_login():
    pass
```

## Fixtures & Setup

Use pytest fixtures for reusable test data:

```python
import pytest

@pytest.fixture
def sample_user():
    """Fixture providing a valid user object."""
    return {"name": "Jane Doe", "email": "jane@example.com"}

@pytest.fixture
def empty_database(tmp_path):
    """Fixture providing a clean temporary database."""
    db_file = tmp_path / "test.db"
    return db_file

def test_user_creation(sample_user):
    """Test that user is created from fixture data."""
    user = User.create(**sample_user)
    assert user is not None

def test_database_isolation(empty_database):
    """Test that database is isolated per test."""
    assert not empty_database.exists()
```

## Assertions

- Use simple, direct assertions
- Avoid complex logic in assertions
- Use pytest's assertion introspection

```python
# ✅ Good assertions
assert len(users) == 3
assert user.name in ["John", "Jane"]
assert isinstance(result, dict)
assert result["status"] == "active"

# For better error messages
from pytest import approx
assert value == approx(3.14159, rel=1e-5)

# ❌ Bad assertions
assert len(users) > 0 and len(users) < 5
assert result
```

## Exception Testing

Use `pytest.raises` to test exceptions:

```python
import pytest

def test_invalid_email_raises_error():
    """Test that invalid email raises ValueError."""
    with pytest.raises(ValueError, match="Invalid email"):
        User.create(name="John", email="invalid-email")

def test_missing_required_field_raises_error():
    """Test that missing name raises KeyError."""
    with pytest.raises(KeyError):
        User.create(email="john@example.com")
```

## Parametrized Tests

Use `@pytest.mark.parametrize` for testing multiple inputs:

```python
@pytest.mark.parametrize("input_value,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (0, 0),
    (-1, -2),
])
def test_double_values(input_value, expected):
    """Test that double() returns value times 2."""
    assert double(input_value) == expected

@pytest.mark.parametrize("email", [
    "valid@example.com",
    "user+tag@example.co.uk",
    "test.email@domain.org",
])
def test_valid_email_formats(email):
    """Test that valid emails pass validation."""
    assert is_valid_email(email) is True
```

## Test Coverage

- Aim for >80% code coverage
- Cover happy paths, edge cases, and error conditions
- Use `pytest-cov` for coverage reporting

```bash
pytest --cov=src --cov-report=html tests/
```

## Mocking & Isolation

Mock external dependencies:

```python
from unittest.mock import Mock, patch

@patch('requests.get')
def test_fetch_user_from_api(mock_get):
    """Test API call returns expected user data."""
    mock_get.return_value.json.return_value = {"id": 1, "name": "John"}
    
    result = fetch_user_from_api(user_id=1)
    
    assert result["name"] == "John"
    mock_get.assert_called_once_with("https://api.example.com/users/1")

def test_database_isolation(mocker):
    """Test without hitting real database."""
    mock_db = mocker.patch('myproject.db.connect')
    mock_db.return_value.query.return_value = []
    
    result = get_users()
    assert result == []
```

## Test Class Organization

Group related tests in classes:

```python
class TestUserValidation:
    """Tests for user input validation."""
    
    def test_valid_name_passes(self):
        assert validate_name("John Doe") is True
    
    def test_empty_name_fails(self):
        assert validate_name("") is False

class TestUserCreation:
    """Tests for user creation workflow."""
    
    def test_user_created_with_valid_data(self):
        user = User.create(name="John", email="john@example.com")
        assert user.id is not None
```

## Markers for Test Organization

Use pytest markers for categorizing tests:

```python
@pytest.mark.slow
def test_long_running_operation():
    pass

@pytest.mark.integration
def test_database_connection():
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass
```

Run specific test categories:
```bash
pytest -m "not slow"
pytest -m integration
```
