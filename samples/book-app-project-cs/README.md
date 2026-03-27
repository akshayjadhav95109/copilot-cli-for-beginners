# Book Collection App

*(This README is intentionally rough so you can improve it with GitHub Copilot CLI)*

A C# console app for managing books you have or want to read.
It can add, remove, and list books. Also mark them as read.

---

## Current Features

* Reads books from a JSON file (our database)
* Validates publication years (1000-2100 range)
* Prompts user to re-enter invalid years instead of silently failing
* Validates years when loading from JSON file
* Some tests exist but probably not enough

---

## Input Validation

### Year Validation
Publication years must be between **1000 and 2100** (inclusive). This range:
- Supports historical books (e.g., 1000-1900)
- Supports modern publications (1900-2024)
- Supports near-future releases up to 2100
- Rejects unrealistic years (negative, year 0, or beyond 2100)

**User Experience:**
- When adding a book: If you enter an invalid year, the app displays a clear error and asks you to try again
- When loading from JSON: Books with invalid years are skipped with a warning

**Examples:**
```bash
Year: 0
Error: Year 0 is too early. Please enter a year >= 1000.

Year: 2101
Error: Year 2101 is too late. Please enter a year <= 2100.

Year: 1949
✓ Accepted
```

---

## Files

* `Program.cs` - Main CLI entry point
* `Models/Book.cs` - Book model class
* `Services/BookCollection.cs` - BookCollection class with data logic
* `Services/YearValidator.cs` - Year validation logic
* `data.json` - Sample book data
* `Tests/BookCollectionTests.cs` - xUnit tests for book operations
* `Tests/YearValidationTests.cs` - xUnit tests for year validation

---

## Running the App

```bash
dotnet run -- list
dotnet run -- add
dotnet run -- find
dotnet run -- remove
dotnet run -- help
```

## Running Tests

```bash
cd Tests
dotnet test
```

---

## Notes

* Not production-ready (obviously)
* Some code could be improved
* Could add more commands later
