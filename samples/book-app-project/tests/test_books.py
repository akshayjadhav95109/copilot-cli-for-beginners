import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    success, message = collection.remove_book("The Hobbit")
    assert success is True
    assert "removed successfully" in message
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    success, message = collection.remove_book("Nonexistent Book")
    assert success is False
    assert "not found" in message

def test_remove_book_case_insensitive():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    success, message = collection.remove_book("DUNE")
    assert success is True
    assert collection.find_book_by_title("Dune") is None

def test_remove_book_whitespace_tolerant():
    collection = BookCollection()
    collection.add_book("Foundation", "Isaac Asimov", 1951)
    success, message = collection.remove_book("  Foundation  ")
    assert success is True
    assert collection.find_book_by_title("Foundation") is None

def test_remove_book_with_suggestions():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Dune Messiah", "Frank Herbert", 1969)
    success, message = collection.remove_book("Messiah")
    assert success is False
    assert "Did you mean one of:" in message
    assert "Dune Messiah" in message

def test_remove_book_empty_title():
    collection = BookCollection()
    success, message = collection.remove_book("")
    assert success is False
    assert "cannot be empty" in message

def test_find_by_author_whitespace_tolerant():
    collection = BookCollection()
    collection.add_book("Foundation", "Isaac Asimov", 1951)
    collection.add_book("I, Robot", "Isaac Asimov", 1950)
    books = collection.find_by_author("  Isaac Asimov  ")
    assert len(books) == 2
    assert all(b.author == "Isaac Asimov" for b in books)

def test_find_by_author_case_insensitive():
    collection = BookCollection()
    collection.add_book("Foundation", "Isaac Asimov", 1951)
    books = collection.find_by_author("ISAAC ASIMOV")
    assert len(books) == 1
    assert books[0].title == "Foundation"
