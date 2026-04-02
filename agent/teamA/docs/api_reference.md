# Agent Team A — API Reference

## Service Overview

Sprint 1 routing agent for the AI Business Intelligence system.
Reads a user query and decides which downstream service should handle it.
No actual service calls are made in Sprint 1.

---

## Endpoint

### POST /agent/analyze

Routes a user query to the correct service module.

**Request**

```json
{
  "query": "analyze customer reviews"
}
```

| Field | Type   | Required | Description              |
|-------|--------|----------|--------------------------|
| query | string | Yes      | Plain-text user query    |

**Response**

```json
{
  "action": "nlp"
}
```

| Field   | Type   | Description                                      |
|---------|--------|--------------------------------------------------|
| action  | string | Resolved module: `nlp`, `ml`, `cv`, or `unknown` |

**Routing Rules**

| Module  | Trigger Keywords                                              |
|---------|---------------------------------------------------------------|
| nlp     | review, feedback, sentiment, opinion, comment, text          |
| ml      | sales, revenue, trend, data, performance, product, profit, analytics |
| cv      | image, photo, picture, visual, cv, object                    |
| unknown | None of the above matched                                     |

**Error Response** — empty query

```json
{
  "detail": "Field 'query' must not be empty"
}
```

HTTP Status: `400 Bad Request`

---

## Health Check

### GET /

```json
{
  "status": "Agent Team A is running",
  "sprint": 1,
  "endpoint": "POST /agent/analyze"
}
```

---

## API Contract Compliance

| Rule                        | Status |
|-----------------------------|--------|
| Endpoint name matches       | Pass   |
| Input field is `query`      | Pass   |
| Output contains `action`    | Pass   |
| Returns JSON                | Pass   |
| No API calls in Sprint 1    | Pass   |
