#!/usr/bin/env python3
"""Quick test to verify remove_book() improvements."""

import tempfile
import os
import sys

# Create a temporary directory for testing
with tempfile.TemporaryDirectory() as tmpdir:
    # Point to temp data file
    import books
    books.DATA_FILE = os.path.join(tmpdir, "data.json")
    
    # Import after setting DATA_FILE
    from books import BookCollection
    
    collection = BookCollection()
    
    print("Testing improved remove_book() function:")
    print("=" * 60)
    
    # Test 1: Basic removal
    print("\n1. Basic removal:")
    collection.add_book("Dune", "Frank Herbert", 1965)
    success, message = collection.remove_book("Dune")
    print(f"   remove_book('Dune') → {success}, '{message}'")
    assert success and "removed successfully" in message
    
    # Test 2: Case-insensitive matching
    print("\n2. Case-insensitive matching:")
    collection.add_book("Foundation", "Isaac Asimov", 1951)
    success, message = collection.remove_book("FOUNDATION")
    print(f"   remove_book('FOUNDATION') → {success}, '{message}'")
    assert success and "removed successfully" in message
    
    # Test 3: Whitespace tolerance
    print("\n3. Whitespace tolerance:")
    collection.add_book("1984", "George Orwell", 1949)
    success, message = collection.remove_book("  1984  ")
    print(f"   remove_book('  1984  ') → {success}, '{message}'")
    assert success and "removed successfully" in message
    
    # Test 4: Not found - with suggestions
    print("\n4. Not found - with partial match suggestions:")
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Dune Messiah", "Frank Herbert", 1969)
    success, message = collection.remove_book("Messiah")
    print(f"   remove_book('Messiah') → {success}")
    print(f"   Message: '{message}'")
    assert not success and "Did you mean one of:" in message
    
    # Test 5: Not found - no suggestions
    print("\n5. Not found - no suggestions:")
    success, message = collection.remove_book("Unknown Book")
    print(f"   remove_book('Unknown Book') → {success}, '{message}'")
    assert not success and "not found in collection" in message
    
    # Test 6: Empty title
    print("\n6. Empty title edge case:")
    success, message = collection.remove_book("")
    print(f"   remove_book('') → {success}, '{message}'")
    assert not success and "cannot be empty" in message
    
    # Test 7: Whitespace-only title
    print("\n7. Whitespace-only title edge case:")
    success, message = collection.remove_book("   ")
    print(f"   remove_book('   ') → {success}, '{message}'")
    assert not success and "cannot be empty" in message

print("\n" + "=" * 60)
print("✓ All tests passed! The improved remove_book() function:")
print("  • Handles case-insensitive matching")
print("  • Strips leading/trailing whitespace")
print("  • Returns detailed feedback messages")
print("  • Suggests similar titles when not found")
print("  • Validates empty input")
