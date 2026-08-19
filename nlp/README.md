# DocuMind NLP Microservice

## Overview

The NLP microservice performs Natural Language Processing on extracted document text.

### Features

- Text preprocessing
- Document summarization
- Keyword extraction
- Named Entity Recognition (NER)
- Sentiment analysis
- Topic detection
- Recommendation generation
- Mistral LLM enhancement

## API

### POST

```
/nlp/analyze
```

### Request

```json
{
    "query":"Summarize this report",
    "content":"Document text...",
    "metadata":{}
}
```

### Response

```json
{
    "module":"nlp",
    "success":true,
    "summary":"...",
    "keywords":[],
    "entities":[],
    "sentiment":"Positive",
    "topics":[],
    "recommendations":[],
    "message":"NLP analysis completed successfully."
}
```