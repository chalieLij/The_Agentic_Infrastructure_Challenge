# OpenClaw Integration Specs

## Overview
This document outlines the protocol for agents to announce their operational status to the wider swarm network using the OpenClaw compatibility layer.

## Status Announcement Protocol

### 1. State Definitions
*   **AVAILABLE**: The agent is idle and ready to accept new tasks from the queue.
*   **BUSY**: The agent is currently executing a task (generation, rendering, or interaction).
*   **OFFLINE**: The agent is disconnected or in maintenance mode.

### 2. Publication Mechanism
Agents must publish their status to the shared Redis instance using the `PUBSUB` mechanism on the `swarm:heartbeat` channel.

**Heartbeat Message Format (JSON):**
```json
{
  "agent_id": "uuid-string",
  "status": "AVAILABLE", // or "BUSY", "OFFLINE"
  "timestamp": "iso8601-string",
  "current_load": 0.05, // CPU load normalized 0-1
  "capabilities": ["video-gen", "trend-analysis"]
}
```

### 3. Registry Updates
Upon receiving a heartbeat:
1.  The `NetworkManager` updates the agent's entry in the `active_agents` hash map.
2.  Sets a generic TTL (e.g., 30 seconds) on the entry. If no heartbeat is received within the TTL, the agent is presumed dead and removed from the active pool.
