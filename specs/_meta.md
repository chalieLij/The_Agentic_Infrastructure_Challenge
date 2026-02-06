# Project Chimera: High-Level Vision

## Overview
Project Chimera is an Autonomous Influencer System designed to generate, review, and publish content independently while maintaining high engagement and brand safety. By orchestrating a swarm of specialized AI agents, the system simulates a creative studio workflow—spanning ideation, asset generation, quality assurance, and community interaction.

## Core Objectives
1.  **Autonomy**: Minimize human intervention in the standard content loop (Idea -> Post).
2.  **Personality Consistency**: Ensure all outputs align with the defining "Agent Persona" (voice, beliefs, visual style).
3.  **Economic Viability**: Operate within strict financial boundaries for compute and blockchain resource usage.
4.  **Safety & Alignment**: Prevent the dissemination of harmful, low-quality, or off-brand content through rigorous multi-layer validation.

## Strategic Constraints

### 1. Budget Caps
*   **Daily Spend Limit**: A strict implementation of a "Dead Man's Switch" for financial operations. The system must not exceed a predefined daily budget (e.g., $50.00 USDC) for transaction fees and paid API services.
*   **Resource Throttling**: Generation tasks must pause if projected costs for the remainder of the cycle exceed allocated reserves.

### 2. Human-in-the-Loop (HITL) for Sensitive Content
*   **Confidence Thresholds**: Any task result with a confidence score falling between the "Rejection" threshold (e.g., 0.7) and the "Auto-Approval" threshold (e.g., 0.9) must be routed to a human reviewer.
*   **Sensitive Topics**: Content flagged as potentially controversial, political, or brand-risky by the safety filters must explicitly require human sign-off, regardless of the internal confidence score.
*   **Financial Approvals**: Transactions exceeding a secondary "high-value" threshold (e.g., >$10.00 USDC single transaction) require manual confirmation.

### 3. Latency & Reliability
*   **Asynchronous Architecture**: The system must handle long-running generation tasks (e.g., video rendering) without blocking the core control loop.
*   **State Recovery**: In the event of a crash, the system must recover its global state (active agents, campaign progress) from the persistence layer (Redis) with zero data loss.

## System Architecture Highlights
*   **Swarm Intelligence**: Decentralized workers (Agents) pulling tasks from a central queue.
*   **Optimistic Concurrency**: Global state management ensuring data integrity during high-concurrency updates.
*   **Cognitive Core**: A context-aware assembly engine that dynamically builds system prompts based on persona directives and recalled memories.
