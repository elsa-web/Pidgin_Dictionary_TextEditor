# Pidgin Lexer API Documentation

## Overview
This API analyzes a sentence and detects language issues for Nigerian Pidgin English.

Detected categories:
- SPELLING: Misspelled words with correction guidance.
- SYNTAX: English grammar structures used instead of Pidgin patterns.
- SEMANTIC: English words where a Pidgin equivalent is expected.
- UNKNOWN: Token not found in the lexicon.

## Endpoint
- Method: POST
- URL: /api/lexer/analyze/
- Content-Type: application/json

## Request Body
```json
{
  "sentence": "I am going to the market"
}
```

Rules:
- sentence is required.
- sentence must be a non-empty string.

## Success Response
Status: 200 OK

```json
{
  "sentence": "I am going to the market",
  "tokens": [
    {
      "raw": "I",
      "type": "PRONOUN",
      "lower": "i"
    },
    {
      "raw": "am",
      "type": "PRONOUN",
      "lower": "am"
    },
    {
      "raw": "going",
      "type": "UNKNOWN",
      "lower": "going"
    },
    {
      "raw": "to",
      "type": "PREPOSITION",
      "lower": "to"
    },
    {
      "raw": "the",
      "type": "UNKNOWN",
      "lower": "the"
    },
    {
      "raw": "market",
      "type": "UNKNOWN",
      "lower": "market"
    }
  ],
  "errors": [
    {
      "type": "SYNTAX",
      "word": "I am going to the market",
      "message": "English grammar pattern detected",
      "suggestion": "I de go market"
    },
    {
      "type": "UNKNOWN",
      "word": "going",
      "message": "Word \"going\" not found in lexicon",
      "suggestion": "—"
    }
  ],
  "summary": {
    "total_tokens": 6,
    "total_errors": 2,
    "error_types": ["SYNTAX", "UNKNOWN"],
    "status": "errors_found"
  }
}
```

Note:
- Punctuation is ignored and not included in tokens.
- Tokenization regex used by the service is:
  - ([a-zA-Z'\\-]+|[^a-zA-Z\\s])
- Summary status values:
  - ok: no errors
  - errors_found: one or more errors

## Error Responses
### 400 Bad Request (missing sentence)
```json
{
  "error": "sentence field is required"
}
```

### 400 Bad Request (invalid JSON)
```json
{
  "error": "Invalid JSON"
}
```

### 405 Method Not Allowed
```json
{
  "error": "Method not allowed"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal lexer error",
  "detail": "<server error details>"
}
```

## Curl Example
```bash
curl -X POST http://127.0.0.1:8000/api/lexer/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"sentence":"I am going to the market"}'
```
