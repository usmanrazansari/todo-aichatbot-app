# Implementation Plan: AI-Powered Chatbot via MCP

**Branch**: `001-ai-chatbot-mcp` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ai-chatbot-mcp/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Extend the Phase II Todo application with an AI-powered conversational interface that enables natural language task management. The system uses a stateless backend architecture where an OpenAI Agents SDK-orchestrated AI agent invokes MCP (Model Context Protocol) tools to perform task operations. Conversations are persisted in the database and reconstructed on each request, ensuring the backend remains stateless while providing continuous conversation context. The frontend integrates OpenAI ChatKit for the chat UI, connecting to a new `/api/{user_id}/chat` endpoint that handles authentication, conversation persistence, AI orchestration, and tool execution.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/JavaScript (frontend with Next.js)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, OpenAI Agents SDK, MCP SDK (Python), Better Auth (existing)
- Frontend: Next.js, React, OpenAI ChatKit, existing Phase II dependencies
**Storage**: SQLite (existing, extended with Conversation and Message tables)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (Linux/Windows server for backend, modern browsers for frontend)
**Project Type**: Web (frontend + backend monorepo)
**Performance Goals**:
- Chat endpoint response < 3 seconds (excluding AI model latency)
- Database conversation history retrieval < 500ms
- Support 50+ message conversation history without degradation
**Constraints**:
- Backend must remain stateless (no in-memory session storage)
- All task operations must go through MCP tools (no direct DB access from AI agent)
- Conversation history limited to 50 messages or 30 days
- JWT authentication required for all chat requests
**Scale/Scope**:
- Single-user hackathon demo (extensible to multi-user production)
- 5 MCP tools (add, list, update, complete, delete tasks)
- 2 new database tables (Conversation, Message)
- 1 new API endpoint (chat)
- 1 new frontend page/component (chat interface)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Note**: The constitution file at `.specify/memory/constitution.md` is a template placeholder. Since no project-specific constitution exists, we proceed with standard software engineering best practices:

### Standard Best Practices Applied

✅ **Separation of Concerns**: AI orchestration logic separated from business logic (MCP tools)
✅ **Stateless Architecture**: Backend maintains no in-memory state; all state persisted to database
✅ **Security**: JWT authentication enforced at API layer; user ownership validated in MCP tools
✅ **Testability**: MCP tools independently testable; clear interfaces between components
✅ **Simplicity**: Minimal viable implementation; no premature optimization
✅ **Existing Patterns**: Reuses Phase II authentication, database, and service layer patterns

### Complexity Justification

No violations to justify. The architecture follows standard patterns:
- Stateless API design (industry standard)
- Tool-based AI agent architecture (MCP protocol standard)
- Database-backed persistence (standard web app pattern)

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chatbot-mcp/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (to be created)
├── data-model.md        # Phase 1 output (to be created)
├── quickstart.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output (to be created)
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoint
│   └── mcp-tools.json   # MCP tool schemas
├── checklists/          # Quality validation
│   └── requirements.md  # Spec validation checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py              # Existing Phase II
│   │   ├── conversation.py      # NEW: Conversation model
│   │   └── message.py           # NEW: Message model
│   ├── services/
│   │   ├── task_service.py      # Existing Phase II
│   │   ├── conversation_service.py  # NEW: Conversation CRUD
│   │   └── message_service.py   # NEW: Message CRUD
│   ├── api/
│   │   ├── task_routes.py       # Existing Phase II
│   │   ├── auth_routes.py       # Existing Phase II
│   │   └── chat_routes.py       # NEW: Chat endpoint
│   ├── ai/
│   │   ├── agent.py             # NEW: OpenAI Agents SDK integration
│   │   └── prompts.py           # NEW: System prompts for agent
│   ├── mcp/
│   │   ├── server.py            # NEW: MCP server implementation
│   │   └── tools/               # NEW: MCP tool implementations
│   │       ├── add_task.py
│   │       ├── list_tasks.py
│   │       ├── update_task.py
│   │       ├── complete_task.py
│   │       └── delete_task.py
│   ├── db/
│   │   └── database.py          # Existing (may need minor updates)
│   ├── utils/
│   │   └── jwt_handler.py       # Existing Phase II
│   └── main.py                  # Existing (add chat routes)
└── tests/
    ├── unit/
    │   ├── test_mcp_tools.py    # NEW: Unit tests for MCP tools
    │   ├── test_conversation_service.py  # NEW
    │   └── test_message_service.py       # NEW
    ├── integration/
    │   ├── test_chat_endpoint.py         # NEW: Integration tests
    │   └── test_agent_mcp_flow.py        # NEW: End-to-end AI flow
    └── contract/
        └── test_mcp_tool_schemas.py      # NEW: Schema validation

frontend/
├── src/
│   ├── pages/
│   │   ├── dashboard.tsx        # Existing Phase II
│   │   ├── login.tsx            # Existing Phase II
│   │   ├── register.tsx         # Existing Phase II
│   │   └── chat.tsx             # NEW: Chat interface page
│   ├── components/
│   │   ├── TaskList.tsx         # Existing Phase II
│   │   ├── TaskForm.tsx         # Existing Phase II
│   │   └── ChatInterface.tsx    # NEW: ChatKit integration
│   ├── services/
│   │   ├── api.ts               # Existing Phase II
│   │   └── chatApi.ts           # NEW: Chat API client
│   └── types/
│       ├── task.ts              # Existing Phase II
│       └── chat.ts              # NEW: Chat types
└── tests/
    └── chat/
        └── ChatInterface.test.tsx  # NEW: Component tests
```

**Structure Decision**: Web application structure (Option 2) selected because the feature extends an existing full-stack web application with separate frontend and backend. The structure preserves Phase II organization while adding new AI/MCP-specific directories (`backend/src/ai/`, `backend/src/mcp/`) to maintain clear separation of concerns.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations identified. Architecture follows standard patterns and project constitution is not yet defined.

## Phase 0: Research & Technical Discovery

### Research Questions

The following technical unknowns must be resolved before design phase:

1. **OpenAI Agents SDK Integration**
   - How does the OpenAI Agents SDK work with custom tools?
   - What is the API for registering and invoking tools?
   - How to pass conversation context to the agent?
   - Error handling patterns for agent failures?

2. **MCP SDK (Model Context Protocol)**
   - What is the official Python MCP SDK package name and installation?
   - How to implement an MCP server in Python?
   - MCP tool schema format and validation?
   - How does OpenAI Agents SDK connect to MCP servers?

3. **OpenAI ChatKit Frontend Integration**
   - What is OpenAI ChatKit and how to integrate it with React/Next.js?
   - Configuration requirements (API keys, domain allowlist)?
   - How to connect ChatKit to custom backend endpoints?
   - Conversation state management in ChatKit?

4. **Stateless Conversation Context**
   - Best practices for reconstructing conversation context from database?
   - Optimal message history size for AI context window?
   - Pagination vs. truncation strategies?
   - Performance optimization for context retrieval?

5. **Database Schema Design**
   - Conversation and Message table relationships?
   - Indexing strategy for fast conversation retrieval?
   - How to handle conversation metadata (tool calls, timestamps)?
   - Migration strategy for adding new tables to existing SQLite database?

### Research Approach

For each research question, I will:
1. Search for official documentation and best practices
2. Identify recommended patterns and anti-patterns
3. Document decisions with rationale
4. Note any assumptions or constraints

**Output**: `research.md` with consolidated findings

## Phase 1: Design & Contracts

### Phase 1 Deliverables

1. **data-model.md**: Database schema for Conversation and Message models
2. **contracts/chat-api.yaml**: OpenAPI specification for chat endpoint
3. **contracts/mcp-tools.json**: MCP tool schemas (5 tools)
4. **quickstart.md**: Developer setup and testing guide
5. **Agent context update**: Update `.claude/settings.local.json` or equivalent with Phase III context

### Design Principles

- **Reuse Phase II patterns**: Follow existing SQLModel patterns, JWT auth flow, service layer structure
- **Clear boundaries**: AI agent ↔ MCP tools ↔ database (no shortcuts)
- **Testability**: Each layer independently testable
- **Stateless**: No in-memory state; all context from database

## Phase 2: Task Breakdown

**Note**: Phase 2 (task generation) is handled by the `/sp.tasks` command, NOT by `/sp.plan`.

After Phase 1 design is complete, run:
```bash
/sp.tasks
```

This will generate `specs/001-ai-chatbot-mcp/tasks.md` with granular, testable implementation tasks.

## Implementation Strategy

### Incremental Development Order

1. **Foundation** (P1 - Critical Path)
   - Database models (Conversation, Message)
   - Conversation/Message service layer
   - Database migrations

2. **MCP Layer** (P1 - Critical Path)
   - MCP server setup
   - Implement 5 MCP tools (reusing existing task service)
   - Unit tests for each tool

3. **AI Agent** (P1 - Critical Path)
   - OpenAI Agents SDK integration
   - Agent configuration with MCP tools
   - System prompts for task management

4. **Chat API** (P1 - Critical Path)
   - Chat endpoint implementation
   - JWT authentication integration
   - Conversation persistence logic
   - Integration tests

5. **Frontend** (P2 - User Interface)
   - ChatKit integration
   - Chat page/component
   - API client for chat endpoint
   - Component tests

6. **Testing & Validation** (P3 - Quality Assurance)
   - End-to-end tests
   - Error handling scenarios
   - Performance validation
   - Security testing

### Risk Mitigation

1. **MCP SDK Unknown**: If official Python MCP SDK doesn't exist or is incompatible, implement MCP protocol manually using JSON-RPC patterns
2. **OpenAI Agents SDK Complexity**: Start with simple tool invocation; add complexity incrementally
3. **ChatKit Integration Issues**: Have fallback plan to build custom chat UI using existing React components
4. **Performance**: Monitor conversation retrieval performance; add database indexes if needed

## Dependencies & Integration Points

### External Dependencies (New)

- `openai-agents-sdk` (or equivalent OpenAI SDK with agent support)
- `mcp-sdk-python` (or equivalent MCP SDK)
- `openai-chatkit` (frontend library)

### Internal Dependencies (Existing Phase II)

- `backend/src/models/task.py` - Task model (reused by MCP tools)
- `backend/src/services/task_service.py` - Task CRUD operations (reused by MCP tools)
- `backend/src/utils/jwt_handler.py` - JWT authentication (reused by chat endpoint)
- `backend/src/db/database.py` - Database engine and session management

### Integration Points

1. **Chat Endpoint → AI Agent**: Pass user message and conversation history
2. **AI Agent → MCP Server**: Invoke tools based on intent
3. **MCP Tools → Task Service**: Reuse existing CRUD operations
4. **Chat Endpoint → Conversation Service**: Persist messages
5. **Frontend ChatKit → Chat API**: HTTP requests with JWT token

## Success Criteria Validation

The implementation will be considered successful when:

1. ✅ Users can create, view, update, complete, and delete tasks via natural language chat
2. ✅ AI agent correctly interprets intent and invokes MCP tools (90%+ accuracy on clear requests)
3. ✅ Conversations persist across sessions and server restarts
4. ✅ Backend remains stateless (verified by restart test)
5. ✅ MCP tools pass independent unit tests
6. ✅ Chat endpoint responds within 3 seconds (excluding AI latency)
7. ✅ All task operations enforce user ownership
8. ✅ Clear traceability: spec → plan → tasks → code

## Next Steps

1. **Execute Phase 0**: Generate `research.md` by researching technical unknowns
2. **Execute Phase 1**: Generate data models, API contracts, and quickstart guide
3. **Run `/sp.tasks`**: Generate granular implementation tasks
4. **Run `/sp.implement`**: Execute tasks via Claude Code

**Current Status**: Plan complete. Ready for Phase 0 research.
