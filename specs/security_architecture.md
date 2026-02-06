# Security Architecture & Containment Protocols

## 1. Authentication & Authorization (AuthN/AuthZ)

### 1.1. Identity Strategy
*   **Protocol**: OAuth 2.0 + OIDC.
*   **Token Standard**: JWT (JSON Web Tokens) with RS256 signing.
*   **Identity Provider (IdP)**: Internal Mock (Phase 1) -> Auth0/Keycloak (Phase 2).

### 1.2. Token Lifecycle
*   **Access Token**: TTL 15 minutes. Stateless validation via signature.
*   **Refresh Token**: TTL 24 hours. Rotated on use. Stored in HTTP-only, Secure cookies.
*   **Scope Pattern**: `service:resource:action` (e.g., `agent:task:execute`).

### 1.3. Role-Based Access Control (RBAC)

| Role | Description | Permissions (Scopes) |
| :--- | :--- | :--- |
| **Orchestrator** | The "Brain" managing the swarm. | `swarm:manage`, `agent:create`, `task:assign` |
| **Agent** | An autonomous worker node. | `task:read`, `content:write`, `trend:read` |
| **Auditor** | Human oversight / Telemetry. | `audit:read`, `logs:read` |
| **System** | Internal cron/maintenance. | `db:migrate`, `cache:clear` |

## 2. Secrets Management & Environment

*   **Principle**: "Zero Trust" for code repositories.
*   **Storage**:
    *   **Development**: `.env` file (gitignored).
    *   **Production**: HashiCorp Vault or AWS Secrets Manager.
*   **Injection**: Secrets are injected as Environment Variables at runtime container startup.
*   **Hardcoding Policy**: CI/CD pipeline fails if high-entropy strings are detected in commit history (TruffleHog).

## 3. Agent Containment Boundaries (The "Sandbox")

To prevent "runaway" agent behavior, the following strict boundaries are enforced at the network/OS level:

### 3.1. Network Egress Whitelist
Agents may ONLY connect to specific, whitelisted domains. All other traffic is dropped by the Docker network firewall.
*   `api.twitter.com` (Social API)
*   `api.openai.com` (LLM Inference)
*   `internal-redis:6379` (OpenClaw Bus)
*   `internal-postgres:5432` (Persistence)

### 3.2. Filesystem Restrictions
*   **Root FS**: Read-Only (`read_only: true`).
*   **Temp Volume**: `/tmp/workspace` is the ONLY writable directory.
*   **Cleanup**: The `/tmp/workspace` volume is wiped after every `AgentTask` completion.

## 4. Content Moderation Pipeline

Before any content is published to social platforms, it must pass the Safety Gate.

### 4.1. Automated Filters (Pre-Flight)
Every generated artifact is scored against these thresholds:
*   **Hate Speech**: < 0.01
*   **Self-Harm**: < 0.01
*   **Sexual Content**: < 0.05
*   **Political Bias**: < 0.20

### 4.2. Human-in-the-Loop (Escalation)
*   **Green Lane**: Scores below all thresholds -> Auto-Publish.
*   **Red Lane**: Scores above threshold -> Status set to `REVIEW_REQUIRED`.
*   **Mechanism**: The item is pushed to a "Human Review Queue" in the Dashboard. The Agent pauses until manual approval.

## 5. Rate Limiting (API Protection)
Implemented via Redis Token Bucket algorithm.

*   **Global**: 1000 req/min per IP.
*   **Agent**: 60 req/min per `agent_id` (Prevents spam loops).
*   **Trend Fetcher**: 10 req/hour (Expensive external API).

## 6. Implementation Guide for AI
When implementing endpoints:
1.  Apply the `@require_scope("scope:name")` decorator.
2.  Validate JWT in the `Authorization` header.
3.  Sanitize all inputs before DB queries (SQLAlchemy handles this, NO raw SQL string formatting).