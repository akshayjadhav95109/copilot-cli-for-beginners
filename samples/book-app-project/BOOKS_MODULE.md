# Books Module Documentation

## Overview

The `books` module provides a simple, persistent book collection manager with case-insensitive search and user-friendly error handling.

## Classes

### `Book`

A dataclass representing a single book in the collection.

**Attributes:**
- `title` (str): Book title
- `author` (str): Author name
- `year` (int): Publication year
- `read` (bool, optional): Whether the book has been read. Defaults to `False`.

**Example:**
```python
book = Book(title="Dune", author="Frank Herbert", year=1965, read=True)
```

---

### `BookCollection`

Manages a collection of books with persistent JSON storage.

**Features:**
- Automatically loads books from `data.json` on initialization
- Saves changes immediately to disk
- Case-insensitive, whitespace-tolerant search
- Helpful suggestions for failed lookups

#### `__init__()`

Initializes a new collection and loads existing books from `data.json`.

**Example:**
```python
collection = BookCollection()  # Loads books from data.json if it exists
```

**Gotcha:** If `data.json` is corrupted, a warning is printed and an empty collection is created.

---

#### `load_books()`

Loads books from the JSON file if it exists.

**Behavior:**
- If `data.json` doesn't exist, initializes an empty collection
- If `data.json` is corrupted, prints a warning and initializes an empty collection
- Silently succeeds if file loads correctly

**Example:**
```python
collection.load_books()  # Reloads from disk (useful after external file changes)
```

---

#### `save_books()`

Saves the current collection to `data.json` (called automatically by mutating methods).

**Example:**
```python
collection.add_book("Foundation", "Isaac Asimov", 1951)
# save_books() is called automatically
```

**Limitation:** Errors during file write (e.g., permission denied, disk full) are not caught. Use in a try-except if reliability is critical.

---

#### `add_book(title: str, author: str, year: int) -> Book`

Adds a new book to the collection and persists to disk.

**Parameters:**
- `title` (str): Book title
- `author` (str): Author name
- `year` (int): Publication year

**Returns:** The `Book` object that was created

**Example:**
```python
book = collection.add_book("1984", "George Orwell", 1949)
print(book.read)  # False (default)
```

---

#### `list_books() -> List[Book]`

Returns all books in the collection.

**Returns:** List of all `Book` objects

**Example:**
```python
books = collection.list_books()
for book in books:
    print(f"{book.title} by {book.author} ({book.year})")
```

---

#### `find_book_by_title(title: str) -> Optional[Book]`

Finds a book by title with case-insensitive, whitespace-tolerant matching.

**Parameters:**
- `title` (str): Title to search for (spaces and case are ignored)

**Returns:** The first matching `Book` object, or `None` if not found

**Example:**
```python
book = collection.find_book_by_title("  DUNE  ")
# Matches "Dune" (case-insensitive, ignores extra spaces)

book = collection.find_book_by_title("Unknown")
print(book)  # None
```

**Limitation:** Returns the first match only. If multiple books have the same title, only one is returned.

---

#### `mark_as_read(title: str) -> bool`

Marks a book as read and persists the change.

**Parameters:**
- `title` (str): Title to search for (case-insensitive, whitespace-tolerant)

**Returns:** `True` if book was found and marked, `False` if book not found

**Example:**
```python
success = collection.mark_as_read("Dune")
if success:
    print("Book marked as read!")
else:
    print("Book not found")
```

---

#### `remove_book(title: str) -> tuple[bool, str]`

Removes a book by title with helpful error messages and suggestions.

**Parameters:**
- `title` (str): Title to search for (case-insensitive, whitespace-tolerant)

**Returns:** Tuple of (success: bool, message: str)
- `(True, "Book '...' removed successfully.")` if book was found and removed
- `(False, "Error: Title cannot be empty.")` if title is empty
- `(False, "Book '...' not found. Did you mean one of: ...")` if no match, but partial matches exist
- `(False, "Book '...' not found in collection.")` if no matches at all

**Example:**
```python
success, message = collection.remove_book("Dune")
print(message)  # "Book 'Dune' removed successfully."

success, message = collection.remove_book("  unknown  ")
print(message)  # "Book 'unknown' not found. Did you mean one of: 'Foundation', 'Dune'?"
```

**Limitation:** Suggestions use substring matching and show up to 3 results. For large collections, suggestion generation may be slow.

---

#### `find_by_author(author: str) -> List[Book]`

Finds all books by a given author with case-insensitive matching.

**Parameters:**
- `author` (str): Author name (case-insensitive, whitespace-tolerant)

**Returns:** List of `Book` objects by that author (empty list if none found)

**Example:**
```python
books = collection.find_by_author("Isaac Asimov")
print(f"Found {len(books)} books by Isaac Asimov")

for book in books:
    print(f"  - {book.title} ({book.year})")
```

**Limitation:** Uses exact author name matching (after normalization). Partial author names won't match.

---

## Utility Functions

### `_normalize_title(title: str) -> str`

Internal helper that normalizes strings for comparison: converts to lowercase and strips whitespace.

**Parameters:**
- `title` (str): String to normalize

**Returns:** Normalized string

**Note:** This is a private function (prefixed with `_`). Don't use it directly; it's for internal use by the module.

---

## File Format

Books are stored in `data.json` in the following format:

```json
[
  {
    "title": "Dune",
    "author": "Frank Herbert",
    "year": 1965,
    "read": true
  },
  {
    "title": "Foundation",
    "author": "Isaac Asimov",
    "year": 1951,
    "read": false
  }
]
```

---

## Usage Example

```python
# Create a collection (loads from data.json if it exists)
collection = BookCollection()

# Add some books
collection.add_book("1984", "George Orwell", 1949)
collection.add_book("Brave New World", "Aldous Huxley", 1932)

# List all books
for book in collection.list_books():
    print(f"{book.title} by {book.author}")

# Find a book (case and whitespace insensitive)
book = collection.find_book_by_title("  1984  ")
print(book.read)  # False

# Mark as read
collection.mark_as_read("1984")

# Find books by author
orwell_books = collection.find_by_author("George Orwell")

# Remove a book
success, message = collection.remove_book("1984")
print(message)
```

---

## Gotchas & Limitations

| Issue | Impact | Workaround |
|-------|--------|-----------|
| **Data loss on corrupt JSON** | Empty collection created without backup | Use version control for `data.json` |
| **No write error handling** | Unhandled exceptions if disk is full or permissions denied | Wrap mutations in try-except if critical |
| **Single match only** | `find_book_by_title()` returns first match if duplicates exist | Use `list_books()` and filter manually |
| **Substring matching in suggestions** | Suggestions may be slow for very large collections | Acceptable for typical use (<10k books) |
| **Exact author matching** | Can't search for partial author names | Use `list_books()` and filter manually |

---

## Type Hints

The module uses Python type hints. All methods are annotated with parameter and return types for IDE autocomplete and type checking.

```python
from typing import List, Optional, Tuple
```

---

## Python Version

The module targets **Python 3.9+**. Note: Some type annotations use `tuple[...]` syntax which requires Python 3.10+. For Python 3.9 compatibility, use `Tuple[...]` from `typing`.
