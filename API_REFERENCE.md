# 🔌 API Reference - MCP Servers

## Overview

All MCP servers expose a standard HTTP API with three endpoints:
- `GET /health` - Health check
- `GET /tools` - Available operations
- `POST /operate` - Execute operation

---

## Math Server (Port 8000)

### Base URL
```
http://localhost:8000
```

### Endpoints

#### GET /health
**Check server health**

Response:
```json
{
  "status": "healthy",
  "service": "math"
}
```

#### GET /tools
**List available operations**

Response:
```json
{
  "tools": [
    {
      "name": "add",
      "description": "Add numbers"
    },
    {
      "name": "subtract",
      "description": "Subtract"
    },
    {
      "name": "multiply",
      "description": "Multiply numbers"
    },
    ...
  ]
}
```

#### POST /operate
**Execute a mathematical operation**

Request:
```json
{
  "operation": "average",
  "args": [[10, 20, 30, 40, 50]],
  "kwargs": {}
}
```

Response:
```json
{
  "operation": "average",
  "result": 30.0,
  "status": "success"
}
```

### Operations

#### 1. **add**
Add multiple numbers

```json
{
  "operation": "add",
  "args": [[5, 10, 15]],
  "kwargs": {}
}
```
Response: `{"result": 30}`

#### 2. **subtract**
Subtract two numbers

```json
{
  "operation": "subtract",
  "args": [50, 20],
  "kwargs": {}
}
```
Response: `{"result": 30}`

#### 3. **multiply**
Multiply multiple numbers

```json
{
  "operation": "multiply",
  "args": [[2, 3, 4]],
  "kwargs": {}
}
```
Response: `{"result": 24}`

#### 4. **divide**
Divide two numbers

```json
{
  "operation": "divide",
  "args": [100, 4],
  "kwargs": {}
}
```
Response: `{"result": 25.0}`

#### 5. **average**
Calculate average (mean)

```json
{
  "operation": "average",
  "args": [[10, 20, 30, 40, 50]],
  "kwargs": {}
}
```
Response: `{"result": 30.0}`

#### 6. **median**
Calculate median

```json
{
  "operation": "median",
  "args": [[10, 20, 30, 40, 50]],
  "kwargs": {}
}
```
Response: `{"result": 30}`

#### 7. **sum_numbers**
Sum all numbers

```json
{
  "operation": "sum_numbers",
  "args": [[1, 2, 3, 4, 5]],
  "kwargs": {}
}
```
Response: `{"result": 15}`

#### 8. **max_value**
Find maximum value

```json
{
  "operation": "max_value",
  "args": [[10, 25, 15, 40, 5]],
  "kwargs": {}
}
```
Response: `{"result": 40}`

#### 9. **min_value**
Find minimum value

```json
{
  "operation": "min_value",
  "args": [[10, 25, 15, 40, 5]],
  "kwargs": {}
}
```
Response: `{"result": 5}`

#### 10. **power**
Raise base to exponent

```json
{
  "operation": "power",
  "args": [2, 8],
  "kwargs": {}
}
```
Response: `{"result": 256}`

#### 11. **square_root**
Calculate square root

```json
{
  "operation": "square_root",
  "args": [16],
  "kwargs": {}
}
```
Response: `{"result": 4.0}`

---

## Data Server (Port 8001)

### Base URL
```
http://localhost:8001
```

### Endpoints

#### GET /health
Response:
```json
{
  "status": "healthy",
  "service": "data"
}
```

#### GET /tools
Response:
```json
{
  "tools": [
    {
      "name": "filter_records",
      "description": "Filter records"
    },
    ...
  ]
}
```

#### POST /operate
Execute a data operation

### Operations

#### 1. **filter_records**
Filter records by condition

```json
{
  "operation": "filter_records",
  "args": [
    [{
      "name": "Alice",
      "department": "Engineering",
      "salary": 100000
    }, {
      "name": "Bob",
      "department": "Sales",
      "salary": 75000
    }],
    "department",
    "==",
    "Engineering"
  ],
  "kwargs": {}
}
```

Operators:
- `"=="` - Equal
- `">"` - Greater than
- `"<"` - Less than
- `">="` - Greater or equal
- `"<="` - Less or equal
- `"in"` - In list

Response:
```json
{
  "result": [{
    "name": "Alice",
    "department": "Engineering",
    "salary": 100000
  }]
}
```

#### 2. **group_by**
Group records by field

```json
{
  "operation": "group_by",
  "args": [records, "department"],
  "kwargs": {}
}
```

Response:
```json
{
  "result": {
    "Engineering": [{...}, {...}],
    "Sales": [{...}],
    "HR": [{...}]
  }
}
```

#### 3. **sort_records**
Sort records by field

```json
{
  "operation": "sort_records",
  "args": [records, "salary"],
  "kwargs": {"descending": true}
}
```

Response: `[records sorted by salary (highest first)]`

#### 4. **aggregate**
Aggregate values for a field

```json
{
  "operation": "aggregate",
  "args": [records, "salary", "average"],
  "kwargs": {}
}
```

Operations:
- `"sum"` - Sum values
- `"count"` - Count records
- `"average"` - Average value
- `"max"` - Maximum value
- `"min"` - Minimum value

Response: `{"result": 85000.0}`

#### 5. **select_fields**
Select specific fields

```json
{
  "operation": "select_fields",
  "args": [records, ["name", "salary"]],
  "kwargs": {}
}
```

Response: `[{name: "Alice", salary: 100000}, ...]`

#### 6. **count_records**
Count total records

```json
{
  "operation": "count_records",
  "args": [records],
  "kwargs": {}
}
```

Response: `{"result": 5}`

#### 7. **unique_values**
Get unique values for a field

```json
{
  "operation": "unique_values",
  "args": [records, "department"],
  "kwargs": {}
}
```

Response: `{"result": ["Engineering", "HR", "Sales"]}`

---

## Text Server (Port 8002)

### Base URL
```
http://localhost:8002
```

### Operations

#### 1. **summarize**
Summarize text

```json
{
  "operation": "summarize",
  "args": ["This is a very long text..."],
  "kwargs": {"max_length": 50}
}
```

Response: `{"result": "This is a very long text..."`

#### 2. **extract_entities**
Extract entities from text

Entity types:
- `"numbers"` - Extract numbers
- `"words"` - Split into words
- `"uppercase"` - Extract uppercase words

```json
{
  "operation": "extract_entities",
  "args": ["Hello world 123 test"],
  "kwargs": {"entity_type": "numbers"}
}
```

Response: `{"result": ["123"]}`

#### 3. **classify**
Classify text sentiment

```json
{
  "operation": "classify",
  "args": ["This is great and wonderful"],
  "kwargs": {}
}
```

Response:
```json
{
  "result": {
    "sentiment": "positive",
    "confidence": 0.5,
    "positive_words": 2,
    "negative_words": 0
  }
}
```

#### 4. **word_count**
Count words and analyze

```json
{
  "operation": "word_count",
  "args": ["Hello world test"],
  "kwargs": {}
}
```

Response:
```json
{
  "result": {
    "word_count": 3,
    "character_count": 18,
    "unique_words": 3,
    "average_word_length": 5.2
  }
}
```

#### 5. **format_text**
Format text

Format types:
- `"uppercase"` - UPPERCASE
- `"lowercase"` - lowercase
- `"title"` - Title Case
- `"capitalize"` - Capitalize first letter

```json
{
  "operation": "format_text",
  "args": ["hello world"],
  "kwargs": {"format_type": "uppercase"}
}
```

Response: `{"result": "HELLO WORLD"}`

#### 6. **split_text**
Split text by delimiter

```json
{
  "operation": "split_text",
  "args": ["apple,banana,cherry"],
  "kwargs": {"delimiter": ","}
}
```

Response: `{"result": ["apple", "banana", "cherry"]}`

#### 7. **join_text**
Join text with delimiter

```json
{
  "operation": "join_text",
  "args": [["apple", "banana", "cherry"]],
  "kwargs": {"delimiter": ", "}
}
```

Response: `{"result": "apple, banana, cherry"}`

#### 8. **remove_duplicates**
Remove duplicate strings

```json
{
  "operation": "remove_duplicates",
  "args": [["apple", "banana", "apple", "cherry"]],
  "kwargs": {}
}
```

Response: `{"result": ["apple", "banana", "cherry"]}`

---

## Error Responses

### 404 Not Found
```json
{
  "error": "Unknown operation: invalid_op"
}
```

### 400 Bad Request
```json
{
  "error": "Error message describing the problem"
}
```

### Examples
```json
// Division by zero
{
  "error": "Division by zero"
}

// Empty list operation
{
  "error": "Cannot average empty list"
}

// Invalid field
{
  "error": "Field 'invalid_field' not found"
}
```

---

## Client Libraries

### Python (requests)
```python
import requests

response = requests.post(
    'http://localhost:8000/operate',
    json={
        'operation': 'average',
        'args': [[10, 20, 30]],
        'kwargs': {}
    }
)

result = response.json()
print(result['result'])  # 20.0
```

### JavaScript (fetch)
```javascript
const response = await fetch('http://localhost:8000/operate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    operation: 'average',
    args: [[10, 20, 30]],
    kwargs: {}
  })
});

const result = await response.json();
console.log(result.result);  // 20.0
```

### cURL
```bash
curl -X POST http://localhost:8000/operate \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "average",
    "args": [[10, 20, 30]],
    "kwargs": {}
  }'
```

---

## Rate Limiting

Currently: No built-in rate limiting

Future:
- Implement request throttling
- Add per-agent quotas
- Monitor response times

---

## Versioning

Current API Version: `1.0`

Breaking changes are rare. When they occur:
- Major version (X.0.0) - Breaking changes
- Minor version (1.X.0) - New features
- Patch version (1.0.X) - Bug fixes

---

**For more information, see ARCHITECTURE.md for system design details.**
