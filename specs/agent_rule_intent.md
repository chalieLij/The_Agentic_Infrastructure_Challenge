# Agent Rule Intent Specification (ARI)

## 1. Purpose
This document serves as the **Master Source of Truth** for generating the Agent's operational directives (e.g., `.cursor/rules`, `.github/copilot-instructions.md`, or System Prompts). 
Any modification to the Agent's behavior MUST begin here.

## 2. Project Context
*   **Project Name**: Project Chimera
*   **Domain**: Autonomous Influencer Swarm Infrastructure
*   **Philosophy**: "Velocity via Precision." We avoid hallucination by enforcing strict adherence to executable specifications.

## 3. The Prime Directive
*   **Definition**: The Agent must NEVER generate implementation code without first retrieving and acknowledging the relevant specification file from `specs/`.
*   **Enforcement**: If a user asks "Write a function to X", the Agent must implicitly check: "Do I have a spec for X?"
    *   **Yes**: "According to `specs/functional.md`, here is the plan..."
    *   **No**: "I cannot find a specification for X. Please define the contract in `specs/` first."

## 4. Operational Behaviors

### 4.1. Spec-First Workflow (Traceability)
Before writing any code block, the Agent must output a "Plan Block":
1.  **Context**: "I am implementing User Story #X from `specs/functional.md`."
2.  **Schema**: "I will strictly adhere to the `TrendItem` schema in `specs/technical.md`."
3.  **Persistence**: "Data will be stored using the `TrendSnapshot` model from `specs/database_schema.md`."

### 4.2. Coding Standards
*   **Language**: Python 3.11+
*   **Type Hinting**: Strict `typing` module usage (List, Dict, Optional, etc.).
*   **Testing**: All new logic must be accompanied by a `pytest` test case.
*   **Error Handling**: No bare `except:` clauses. Use specific exceptions defined in contracts.

### 4.3. Forbidden Actions
*   **Vibe Coding**: Guessing variable names or API responses that are not in the spec.
*   **Hardcoding**: No API keys or secrets in code. Use `os.getenv()`.
*   **Scope Creep**: Do not add "nice to have" features not requested in the Prompt or Spec.

## 5. Escalation & Triggers

### 5.1. Ambiguity Trigger
*   **Condition**: The user's prompt contradicts the Spec.
*   **Response**: "Conflict Detected: Your request to add 'author_name' conflicts with the schema in `technical.md` which uses 'agent_id'. Should we update the spec first?"

### 5.2. Safety Trigger
*   **Condition**: Request involves generating non-compliant content (e.g., bypassing safety filters).
*   **Response**: Refuse and cite "Ethical Guidelines Protocol".

## 6. Evolution Strategy
Rules are dynamic based on the project phase:
*   **Phase 1 (Scaffolding)**: Focus on folder structure, config files, and environment setup.
*   **Phase 2 (Implementation)**: Focus on TDD, Pydantic models, and strict Schema compliance.
*   **Phase 3 (Optimization)**: Focus on async performance, indexing, and caching strategies.

*Current Phase: Phase 2 (Implementation)*

## 7. Generation Prompt
*To regenerate the `.cursor/rules` file, use the following prompt:*

> "Act as the Governance Architect. Read `specs/agent_rule_intent.md`. Generate a concise, high-priority `.cursor/rules` file that translates these intents into actionable instructions for the IDE AI. Ensure the 'Prime Directive' is the very first section."