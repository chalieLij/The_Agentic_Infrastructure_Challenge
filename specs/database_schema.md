# Database Architecture & Persistence Strategy

## Technology Stack
*   **Primary Store**: PostgreSQL 16+ (Relational + JSONB)
*   **Cache/PubSub**: Redis (defined in `openclaw_integration.md`)
*   **ORM**: SQLAlchemy (Async)
*   **Migration Manager**: Alembic

## Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    AGENTS ||--o{ AGENT_TASKS : "executes"
    AGENTS ||--o{ CONTENT_ARTIFACTS : "produces"
    AGENT_TASKS ||--o{ CONTENT_ARTIFACTS : "results_in"
    TREND_SNAPSHOTS ||--|{ TREND_ITEMS : "contains"

    AGENTS {
        uuid id PK
        string name
        jsonb persona_config "Serialized AgentPersona"
        string status "AVAILABLE, BUSY, OFFLINE"
        timestamp last_heartbeat
    }

    AGENT_TASKS {
        uuid id PK
        uuid assigned_agent_id FK
        string type "generate, reply, transaction"
        string status "pending, in_progress, completed, failed"
        int priority
        jsonb input_context "The prompt/data"
        jsonb output_result "The artifact refs"
        timestamp created_at
        timestamp updated_at
    }

    TREND_SNAPSHOTS {
        uuid id PK
        string niche "Index: btree"
        string region
        timestamp captured_at
    }

    TREND_ITEMS {
        uuid id PK
        uuid snapshot_id FK
        string keyword
        float sentiment_score
        int search_volume
    }

    CONTENT_ARTIFACTS {
        uuid id PK
        uuid task_id FK
        uuid agent_id FK
        string platform "twitter, youtube"
        string remote_url
        string storage_path
        jsonb metadata "VideoMetadata Object"
    }