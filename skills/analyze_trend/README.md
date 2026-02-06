# Skill: Analyze Trend

## Overview
Fetches and analyzes top trending topics for a specific niche. 
*See `specs/technical.md` for full API details.*

## Input Schema (JSON)
```json
{
  "type": "object",
  "properties": {
    "niche": {
      "type": "string",
      "description": "Category to search (e.g. 'tech', 'finance')."
    },
    "region": {
      "type": "string",
      "default": "US",
      "description": "ISO 3166-1 alpha-2 region code."
    },
    "limit": {
      "type": "integer",
      "default": 10,
      "maximum": 50
    }
  },
  "required": ["niche"]
}
```

## Output Schema (JSON)
```json
{
  "type": "object",
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "niche": { "type": "string" },
    "trends": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "rank": { "type": "integer" },
          "keyword": { "type": "string" },
          "volume": { "type": "integer" },
          "related_hashtags": { "type": "array", "items": { "type": "string" } },
          "sentiment_score": { "type": "number" },
          "source_urls": { "type": "array", "items": { "type": "string" } }
        }
      }
    }
  },
  "required": ["trends", "timestamp"]
}
```
