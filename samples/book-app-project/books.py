import json
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


def _normalize_title(title: str) -> str:
    """Normalize title for comparison: lowercase and strip whitespace."""
    return title.strip().lower()


class BookCollection:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self):
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by title (case-insensitive, whitespace-tolerant)."""
        normalized_search = _normalize_title(title)
        for book in self.books:
            if _normalize_title(book.title) == normalized_search:
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> tuple[bool, str]:
        """
        Remove a book by title. Returns (success, feedback_message).
        
        Examples:
            >>> collection.remove_book("Dune")
            (True, "Book 'Dune' removed successfully.")
            
            >>> collection.remove_book("  Unknown  ")
            (False, "Book 'Unknown' not found. Did you mean one of: 'Dune', 'Foundation'?")
        """
        if not title or not title.strip():
            return False, "Error: Title cannot be empty."
        
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True, f"Book '{book.title}' removed successfully."
        
        # Provide helpful suggestions if no exact match found
        normalized_search = _normalize_title(title)
        suggestions = [
            b.title for b in self.books
            if normalized_search in _normalize_title(b.title)
        ]
        
        if suggestions:
            suggestions_str = "', '".join(suggestions[:3])  # Show up to 3 suggestions
            return False, f"Book '{title}' not found. Did you mean one of: '{suggestions_str}'?"
        
        return False, f"Book '{title}' not found in collection."

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author (case-insensitive, whitespace-tolerant)."""
        normalized_search = _normalize_title(author)
        return [b for b in self.books if _normalize_title(b.author) == normalized_search]
