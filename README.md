# Project Chimera: The Autonomous Influencer System

[![CI Pipeline](https://github.com/chalielijalem/The_Agentic_Infrastructure_Challenge/actions/workflows/main.yml/badge.svg)](https://github.com/chalielijalem/The_Agentic_Infrastructure_Challenge/actions/workflows/main.yml)
[![Spec Status](https://img.shields.io/badge/Specs-Defined-green)](specs/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🦁 Overview
**Project Chimera** is a Swarm-based Autonomous Influencer System. It orchestrates specialized AI agents to generate, review, and publish content independently while maintaining high engagement, brand safety, and economic viability.

Unlike standard chatbots, Chimera is designed as a **long-running infrastructure** that:
*   Manages its own wallet and transaction budgets.
*   Enforces "Dead Man's Switch" financial safety constraints.
*   Syncs global state across a distributed swarm using Optimistic Concurrency Control.
*   Uses a "Judge" agent for QA and Human-in-the-Loop (HITL) escalation.

---

## 🏗 Architecture
The system follows a modular Swarm architecture:

| Component | Description | Key Tech |
| :--- | :--- | :--- |
| **The Brain (Core)** | Concurrency control & prompt assembly. | `Redis`, `Optimistic Locking` |
| **The Swarm** | Task execution loop (Planner -> Worker -> Judge). | `MCP`, `Pydantic` |
| **Commerce** | Blockchain interactions & budget management. | `Coinbase AgentKit`, `Python` |
| **Skills** | Modular capabilities (Trend analysis, Media handling). | `Python`, `APIs` |

### Key Modules
*   **`src/core/state.py`**: Manages the Global State with Versioning and Optimistic Locking (Redis `WATCH` transactions).
*   **`src/swarm/judge.py`**: Validates agent outputs. Automation > 0.9 confidence, HITL for 0.7-0.9, Reject < 0.7.
*   **`src/commerce/wallet.py`**: Handles crypto transactions with strict daily spend limits (e.g., $50 USDC).
*   **`specs/`**: The authoritative source of truth for all Data Schemas and API contracts.

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.9+
*   Docker (for containerized testing)
*   Redis (for state management)

### Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/chalielijalem/The_Agentic_Infrastructure_Challenge.git
    cd The_Agentic_Infrastructure_Challenge
    ```

2.  **Set up the environment**:
    ```bash
    make setup
    ```

3.  **Run Tests (Dockerized)**:
    ```bash
    make test
    ```

---

## 🛠 Tooling Strategy
This project leverages the **Model Context Protocol (MCP)** to integrate AI agents with development tools:
*   **`filesystem-mcp`**: For safe code/spec generation.
*   **`git-mcp`**: For version control operations.
*   **`redis-mcp`**: For inspecting the live swarm state.
*   **`tenxfeedbackanalytics`**: For AI fluency and performance telemetry.

See [`research/tooling_strategy.md`](research/tooling_strategy.md) for details.

---

## 📜 Governance & Compliance
We strictly adhere to a **Spec-First** development philosophy.

*   **The Prime Directive**: NEVER generate code without checking `specs/` first.
*   **CI/CD**: `make test` runs automatically on every push via GitHub Actions.
*   **Code Review**: `.coderabbit.yaml` is configured to check for Spec Alignment and Security Vulnerabilities automatically.

### Documentation Index
*   [**Vision & Constraints**](specs/_meta.md)
*   [**Technical Specs (Schemas/APIs)**](specs/technical.md)
*   [**Functional User Stories**](specs/functional.md)
*   [**Swarm Protocol**](specs/openclaw_integration.md)

---

## 🧪 Current Status
*   **Phase**: Implementation (TDD Cycle)
*   **Implemented**: Scaffolding, Core Specs, Governance, Basic Skills Interfaces.
*   **In Progress**: Implementing Skill logic to pass the current TDD test suite.

---

## 🤝 Contributing
1.  Check the `specs/` for the relevant schema.
2.  Write a failing test case in `tests/`.
3.  Implement the logic in `src/`.
4.  Run `make test` to verify.
5.  Push to `main`.