# Tooling Strategy

## Developer Tools & MCP Servers
To support the autonomous workflow of Project Chimera, the following Model Context Protocol (MCP) servers and developer tools are integrated:

### 1. `filesystem-mcp`
*   **Purpose**: Allows agents to safely read/write code, configuration, and log files within the workspace.
*   **Permissions**: Restricted to the project root.
*   **Key Use Cases**: 
    *   Generating source code (`src/`).
    *   Writing specifications (`specs/`).
    *   saving generated media assets to local volumes.

### 2. `git-mcp`
*   **Purpose**: Enables agents to perform version control operations.
*   **Capabilities**: `git status`, `git add`, `git commit`, `git push`.
*   **Workflow**: Agents must commit their work after passing unit tests.

### 3. `redis-mcp` (Custom/Internal)
*   **Purpose**: Provides direct introspection of the Swarm's global state.
*   **Key Capabilities**:
    *   Viewing active keys (`keys *`).
    *   Reading specific state values (`get global_state`).
    *   Monitoring queues (`lrange review_queue ...`).

### 4. `terminal-mcp` (Built-in)
*   **Purpose**: Execution of shell commands for running builds, tests, and deployment scripts.
*   **Constraints**: Sandbox mode enabled; sensitive env vars redacted in logs.
