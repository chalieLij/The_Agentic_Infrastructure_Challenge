# Technical Specifications

## Data Schemas

### Video Metadata Object (JSON)
The `VideoMetadata` object represents the structured data required to render and publish a video asset.

```jsonc
{
  "title": "string (max 100 chars)",
  "description": "string (max 2200 chars)",
  "tags": ["string"], // Array of strings, max 30 tags
  "aspect_ratio": "string", // Enum: "9:16", "16:9", "1:1"
  "duration_seconds": "number", // Float, e.g., 59.5
  "thumbnail_url": "string (url)",
  "assets": [
    {
      "type": "string", // Enum: "video", "image", "audio"
      "url": "string (url)",
      "layer_index": "integer" // Z-index for compositing (0 is background)
    }
  ],
  "generated_by": {
    "agent_id": "string (uuid)",
    "worker_version": "string (semver)"
  },
  "safety_score": "number" // Float 0.0 - 1.0
}
```

### Agent Task Schema (JSON)
The structure for passing data between Planner and Worker.

```json
{
  "task_id": "uuid-v4-string",
  "task_type": "generate_content | reply_comment | execute_transaction",
  "priority": "high | medium | low",
  "context": {
    "goal_description": "string",
    "persona_constraints": ["string"],
    "required_resources": ["mcp://twitter/mentions/123", "mcp://memory/recent"]
  },
  "assigned_worker_id": "string",
  "created_at": "timestamp",
  "status": "pending | in_progress | review | complete"
}
```

### AgentPersona Model
Used to parse SOUL.md files.

*   **Source**: Markdown file with YAML frontmatter.
*   **Frontmatter Fields**:
    *   `name`: `str`
    *   `id`: `str`
    *   `voice_traits`: `List[str]`
    *   `directives`: `List[str]`
*   **Body Content**: Parsed into a `backstory` field (`str`).

## MCP Tool Interfaces

### post_content
Publishes text and media to a connected social platform.

```json
{
  "name": "post_content",
  "description": "Publishes text and media to a connected social platform.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "platform": {
        "type": "string", 
        "enum": ["twitter", "instagram", "threads"]
      },
      "text_content": {
        "type": "string",
        "description": "The body of the post/tweet."
      },
      "media_urls": {
        "type": "array", 
        "items": {"type": "string"}
      },
      "disclosure_level": {
        "type": "string",
        "enum": ["automated", "assisted", "none"]
      }
    },
    "required": ["platform", "text_content"]
  }
}
```

## API Contracts

### Trend Fetcher Service
**Service Name**: `trend-fetcher`
**Version**: `v1`

#### Endpoint: `GET /trends/current`

Fetches the top trending topics relevant to the agent's niche.

**Request:**
```http
GET /trends/current?niche=tech&region=US&limit=5 HTTP/1.1
Host: api.chimera.internal
Auth-Token: <JWT>
```

**Query Parameters:**
- `niche` (required): `string` - The topic category (e.g., "crypto", "lifestyle").
- `region` (optional): `string` - ISO 3166-1 alpha-2 code (default: "US").
- `limit` (optional): `integer` - Number of results (default: 10, max: 50).

**Response (200 OK):**
```jsonc
{
  "timestamp": "iso8601_string",
  "niche": "tech",
  "trends": [
    {
      "rank": "integer",
      "keyword": "string",
      "volume": "integer", // Estimated search volume
      "related_hashtags": ["string"],
      "sentiment_score": "float", // -1.0 to 1.0
      "source_urls": ["string (url)"]
    }
  ]
}
```

**Error Responses:**
- `400 Bad Request`: Invalid parameters.
- `429 Too Many Requests`: Rate limit exceeded.
- `500 Internal Server Error`: Upstream trend provider failure.
