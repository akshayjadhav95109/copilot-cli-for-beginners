# Data Quality Instructions

These instructions define standards for validating and maintaining JSON data entries across the project.

## JSON File Structure Requirements

### Valid JSON Format

All JSON files must be valid, parseable JSON:

```json
{
  "version": "1.0.0",
  "entries": [
    {
      "id": "entry-001",
      "name": "Sample Entry",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

- Use proper UTF-8 encoding
- No trailing commas
- All strings must be quoted with double quotes
- Valid number formats (no quotes on numbers)

## Required Fields

Every data entry must include these base fields:

```json
{
  "id": "unique-identifier",
  "name": "Human-readable name",
  "description": "What this entry is for",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp",
  "status": "active|inactive|archived"
}
```

### Field Specifications

- **id**: Unique identifier, kebab-case, alphanumeric and hyphens only
  - ✅ `"user-001"`, `"config-main-app"`
  - ❌ `"user_001"`, `"User001"`, `"001"`

- **name**: Required, non-empty string, 1-255 characters
  - ✅ `"Primary Database"`, `"User Authentication Module"`
  - ❌ `""`, `null`

- **description**: Optional but recommended, 0-1000 characters
  - Should explain purpose and scope
  - Use plain English, no HTML

- **created_at / updated_at**: ISO 8601 format with timezone
  - ✅ `"2024-03-27T18:54:08Z"`, `"2024-03-27T18:54:08+00:00"`
  - ❌ `"2024-03-27"`, `"03/27/2024"`, `"1711555248"`

- **status**: One of `active`, `inactive`, or `archived`
  - ✅ `"active"`, `"archived"`
  - ❌ `"pending"`, `"enabled"`, `true`

## Data Validation Rules

### String Fields

- No leading/trailing whitespace
- Consistent casing (PascalCase for names, lowercase for IDs)
- No special characters except where specified
- Max length restrictions must be enforced

```json
{
  "id": "user-john-doe",
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

### Numeric Fields

- Use appropriate number types (no string numbers)
- Define min/max ranges in schema
- Handle zero and negative values appropriately

```json
{
  "user_id": 123,
  "age": 30,
  "balance": 1234.56,
  "score": -5
}
```

### Array Fields

- Consistent element types
- No duplicate IDs within arrays
- Define min/max length

```json
{
  "tags": ["python", "testing", "automation"],
  "ids": [1, 2, 3],
  "nested": [
    {"id": "item-1", "name": "Item 1"},
    {"id": "item-2", "name": "Item 2"}
  ]
}
```

### Date/Time Fields

Always use ISO 8601 format:

```json
{
  "created_at": "2024-03-27T18:54:08Z",
  "updated_at": "2024-03-27T18:54:08Z",
  "due_date": "2024-12-31",
  "event_time": "2024-03-27T18:54:08+05:30"
}
```

### Null Handling

- Prefer omitting optional fields over `null`
- Use `null` only for optional fields
- Never use `null` for required fields

```json
{
  "id": "entry-1",
  "name": "Entry",
  "description": "Optional field - omit instead of using null",
  "notes": null
}
```

## Data Completeness Checklist

For each entry, verify:

- [ ] ID is unique, kebab-case, non-empty
- [ ] Name is present and 1-255 characters
- [ ] All required fields are present
- [ ] No trailing whitespace in string fields
- [ ] Timestamps are ISO 8601 format
- [ ] Status is one of: `active`, `inactive`, `archived`
- [ ] No special characters in IDs
- [ ] Nested objects follow same validation rules
- [ ] Array elements are consistent type
- [ ] No duplicate IDs in related records

## Consistency Rules

### Naming Conventions

Use consistent naming across all entries:

```json
[
  {"field_name": "value"},
  {"field_name": "another_value"}
]
```

- All entries use snake_case for field names
- No mixing of camelCase and snake_case
- Consistent abbreviations (use full names or agreed-upon abbreviations)

### Enum Values

Define and document allowed values:

```json
{
  "status": "active",
  "priority": "high",
  "type": "user"
}
```

Document valid values:
- `status`: `active`, `inactive`, `archived`
- `priority`: `low`, `medium`, `high`, `critical`
- `type`: `user`, `admin`, `guest`

### Related Records

Ensure referential integrity:

```json
[
  {"id": "user-001", "group_id": "group-1"},
  {"id": "user-002", "group_id": "group-1"}
]
```

- All `group_id` references must point to existing groups
- Foreign keys must match the ID format of referenced records
- Remove or update references when parent records are deleted

## Validation Workflow

### Before Committing JSON Files

1. **Format check**: Validate JSON syntax (use `jq` or similar)
2. **Schema validation**: Check against defined schema
3. **Completeness**: Verify all required fields present
4. **Consistency**: Check naming and enum values
5. **Uniqueness**: Ensure no duplicate IDs
6. **Referential integrity**: Verify all references exist

```bash
# Validate JSON syntax
jq empty data.json

# Pretty print for review
jq . data.json

# Check for duplicate IDs
jq '.[] | .id' data.json | sort | uniq -d
```

### Test Data Requirements

Test data files must:
- Follow same validation rules as production data
- Include edge cases (empty strings, max length, etc.)
- Use consistent fixtures across test suite
- Be isolated from production data

```json
{
  "test_users": [
    {
      "id": "test-user-minimal",
      "name": "Minimal",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "status": "active"
    },
    {
      "id": "test-user-max",
      "name": "This is a very long name that tests the maximum length constraint of 255 characters...",
      "description": "Maximum length test entry with full description",
      "created_at": "2024-12-31T23:59:59Z",
      "updated_at": "2024-12-31T23:59:59Z",
      "status": "archived"
    }
  ]
}
```

## Error Messages

When validating data, provide clear error messages:

- ❌ `"Invalid data"`
- ✅ `"ID 'User001' must be kebab-case (e.g., 'user-001')"`
- ✅ `"Required field 'name' missing in entry with ID 'entry-1'"`
- ✅ `"Status 'pending' not allowed. Use: active, inactive, archived"`

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Parse error | Invalid JSON syntax | Validate with `jq empty` |
| Missing field | Required field omitted | Add all required fields |
| Invalid ID | Wrong format (camelCase, spaces) | Use kebab-case: `a-b-c` |
| Bad timestamp | Non-ISO 8601 format | Use format: `2024-03-27T18:54:08Z` |
| Duplicate ID | ID not unique | Ensure each ID is unique |
| Null value | Null in required field | Omit optional fields instead |
