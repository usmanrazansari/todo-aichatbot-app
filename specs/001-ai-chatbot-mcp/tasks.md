# Tasks: AI-Powered Chatbot via MCP

**Input**: Design documents from `/specs/001-ai-chatbot-mcp/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are not explicitly requested in the specification, so test tasks are omitted. Focus is on implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`
- **Frontend**: `frontend/src/`
- **Tests**: `backend/tests/`, `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [x] T001 Install OpenAI Python SDK (openai>=1.0.0) in backend/requirements.txt
- [x] T002 [P] Install MCP SDK (mcp) in backend/requirements.txt or implement MCP protocol manually if SDK unavailable
- [x] T003 [P] Install @chatscope/chat-ui-kit-react in frontend/package.json
- [x] T004 [P] Create backend/src/ai/ directory for AI agent components
- [x] T005 [P] Create backend/src/mcp/ directory for MCP server and tools
- [x] T006 [P] Create backend/src/mcp/tools/ directory for individual MCP tool implementations
- [x] T007 Configure OPENAI_API_KEY environment variable in backend/.env

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Models & Services

- [x] T008 [P] Create Conversation model in backend/src/models/conversation.py with id, user_id, created_at, updated_at, title, archived fields
- [x] T009 [P] Create Message model in backend/src/models/message.py with id, conversation_id, user_id, role, content, created_at, tool_call_id, tool_name fields
- [x] T010 Import Conversation and Message models in backend/src/main.py startup event for auto-migration
- [x] T011 [P] Implement conversation_service.py in backend/src/services/ with create_conversation, get_conversation, list_user_conversations functions
- [x] T012 [P] Implement message_service.py in backend/src/services/ with add_message, get_conversation_history functions

### MCP Server & Tools Foundation

- [x] T013 Initialize MCP server in backend/src/mcp/server.py using official MCP SDK or manual JSON-RPC implementation
- [x] T014 [P] Implement add_task MCP tool in backend/src/mcp/tools/add_task.py calling existing task_service.create_task
- [x] T015 [P] Implement list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py calling existing task_service.get_tasks_by_user_id
- [x] T016 [P] Implement update_task MCP tool in backend/src/mcp/tools/update_task.py calling existing task_service.update_task
- [x] T017 [P] Implement complete_task MCP tool in backend/src/mcp/tools/complete_task.py calling existing task_service.toggle_task_completion
- [x] T018 [P] Implement delete_task MCP tool in backend/src/mcp/tools/delete_task.py calling existing task_service.delete_task
- [x] T019 Register all 5 MCP tools (add, list, update, complete, delete) with MCP server in backend/src/mcp/server.py

### AI Agent Configuration

- [x] T020 Create system prompts in backend/src/ai/prompts.py defining agent role as task management assistant
- [x] T021 Implement AI agent in backend/src/ai/agent.py using OpenAI SDK with function calling, integrating MCP tool schemas
- [x] T022 Implement tool invocation bridge in backend/src/ai/agent.py to convert OpenAI function calls to MCP tool invocations

### Chat API Endpoint

- [x] T023 Create chat_routes.py in backend/src/api/ with POST /api/{user_id}/chat endpoint
- [x] T024 Implement JWT authentication middleware in chat_routes.py reusing existing get_current_user_id from task_routes.py
- [x] T025 Implement conversation context loader in chat_routes.py to fetch/create conversation and retrieve message history
- [x] T026 Implement chat execution logic in chat_routes.py: invoke AI agent, capture tool calls, persist messages, return response
- [x] T027 Register chat_routes router in backend/src/main.py with prefix /api/{user_id}

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks to their todo list by typing natural language messages in a chat interface

**Independent Test**: Send chat message "Add buy groceries to my list" and verify task is created and chatbot confirms

### Implementation for User Story 1

- [x] T028 [US1] Verify add_task MCP tool correctly handles natural language input by testing with sample task titles
- [x] T029 [US1] Verify AI agent correctly interprets "add task" intent and invokes add_task tool with extracted title
- [x] T030 [US1] Implement friendly confirmation response in AI agent for successful task creation
- [x] T031 [US1] Implement clarification request in AI agent for ambiguous task creation requests (e.g., "do the thing")
- [x] T032 [US1] Test chat endpoint with "Add finish the report to my tasks" and verify task creation + confirmation

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create tasks via chat

---

## Phase 4: User Story 2 - View and Complete Tasks via Chat (Priority: P1)

**Goal**: Enable users to see their current tasks and mark them complete using natural language commands

**Independent Test**: Ask "What are my tasks?" and verify tasks are listed, then say "Mark [task] as done" and verify completion

### Implementation for User Story 2

- [x] T033 [US2] Verify list_tasks MCP tool returns tasks in readable format for AI agent
- [x] T034 [US2] Verify complete_task MCP tool correctly marks tasks as completed
- [x] T035 [US2] Implement AI agent logic to format task list in conversational style (numbered list with status)
- [x] T036 [US2] Implement AI agent logic to interpret "list tasks" intent and invoke list_tasks tool
- [x] T037 [US2] Implement AI agent logic to interpret "complete task" intent and invoke complete_task tool with task_id
- [x] T038 [US2] Implement AI agent logic to handle empty task list with friendly message
- [x] T039 [US2] Implement AI agent logic to handle ambiguous task references by asking for clarification
- [x] T040 [US2] Test chat endpoint with "What's on my list?" and verify task listing
- [x] T041 [US2] Test chat endpoint with "Mark buy groceries as complete" and verify task completion + confirmation

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - full read-write cycle via chat

---

## Phase 5: User Story 3 - Update Task Details via Chat (Priority: P2)

**Goal**: Enable users to modify existing task details (title, description) using natural language commands

**Independent Test**: Create a task, then say "Change [task name] to [new name]" and verify task is updated

### Implementation for User Story 3

- [x] T042 [US3] Verify update_task MCP tool correctly handles partial updates (title, description, or both)
- [x] T043 [US3] Implement AI agent logic to interpret "update task" intent and extract task identifier + new values
- [x] T044 [US3] Implement AI agent logic to invoke update_task tool with appropriate parameters
- [x] T045 [US3] Implement AI agent logic to handle task not found error with helpful message
- [x] T046 [US3] Implement friendly confirmation response in AI agent for successful task updates
- [x] T047 [US3] Test chat endpoint with "Change buy milk to buy almond milk" and verify task title update

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently - full CRUD except delete

---

## Phase 6: User Story 4 - Delete Tasks via Chat (Priority: P2)

**Goal**: Enable users to remove tasks from their list using natural language commands with confirmation

**Independent Test**: Say "Delete [task name]" and confirm deletion, verify task is removed

### Implementation for User Story 4

- [x] T048 [US4] Verify delete_task MCP tool correctly removes tasks and returns confirmation
- [x] T049 [US4] Implement AI agent logic to interpret "delete task" intent and identify task to delete
- [x] T050 [US4] Implement AI agent logic to request confirmation before invoking delete_task tool
- [x] T051 [US4] Implement AI agent logic to handle confirmation ("yes") and cancellation ("no") responses
- [x] T052 [US4] Implement friendly confirmation response in AI agent for successful deletion
- [x] T053 [US4] Implement cancellation message in AI agent when user declines deletion
- [x] T054 [US4] Test chat endpoint with "Delete buy groceries" → "yes" and verify task deletion

**Checkpoint**: At this point, User Stories 1-4 should all work independently - complete CRUD operations via chat

---

## Phase 7: User Story 5 - Resume Conversations Across Sessions (Priority: P3)

**Goal**: Enable users to continue their conversation with the chatbot across multiple sessions

**Independent Test**: Start a conversation, close browser, reopen, and verify chat history is restored

### Implementation for User Story 5

- [x] T055 [US5] Verify conversation_service correctly retrieves conversation by conversation_id
- [x] T056 [US5] Verify message_service correctly retrieves conversation history ordered by created_at
- [x] T057 [US5] Implement conversation_id persistence in chat endpoint response
- [x] T058 [US5] Verify chat endpoint correctly resumes existing conversation when conversation_id is provided
- [x] T059 [US5] Verify AI agent receives full conversation history (up to 50 messages) for context
- [x] T060 [US5] Test chat endpoint with new conversation (no conversation_id) and verify new conversation_id is returned
- [x] T061 [US5] Test chat endpoint with existing conversation_id and verify conversation history is loaded

**Checkpoint**: All user stories should now be independently functional - complete Phase III feature set

---

## Phase 8: Frontend Chat Interface

**Purpose**: Build chat UI to connect users to the backend chat endpoint

### Frontend Implementation

- [x] T062 [P] Create chat.tsx page in frontend/src/pages/ with route /chat
- [x] T063 [P] Create ChatInterface.tsx component in frontend/src/components/ using @chatscope/chat-ui-kit-react
- [x] T064 [P] Create chatApi.ts service in frontend/src/services/ with sendMessage function calling POST /api/{user_id}/chat
- [x] T065 [P] Create chat.ts types in frontend/src/types/ defining ChatMessage, ChatRequest, ChatResponse interfaces
- [x] T066 Implement message state management in ChatInterface.tsx (user messages, assistant responses)
- [x] T067 Implement conversation_id persistence in ChatInterface.tsx using localStorage or component state
- [x] T068 Implement JWT token extraction in chatApi.ts from existing auth context
- [x] T069 Implement user_id extraction in chatApi.ts from JWT token for API path
- [x] T070 Implement loading/typing indicator in ChatInterface.tsx while waiting for AI response
- [x] T071 Implement error handling in ChatInterface.tsx for API failures (401, 403, 500)
- [x] T072 Add navigation link to chat page in frontend dashboard or header
- [x] T073 Test frontend chat interface end-to-end: login → navigate to chat → send message → receive response

**Checkpoint**: Frontend chat interface complete and connected to backend

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

### Error Handling & Edge Cases

- [x] T074 [P] Implement error handling in AI agent for OpenAI API failures (rate limits, service unavailable)
- [x] T075 [P] Implement error handling in MCP tools for database failures (connection errors, constraint violations)
- [x] T076 [P] Implement user-friendly error messages in AI agent for all error scenarios
- [x] T077 Implement handling for non-task-related messages in AI agent (greetings, general questions)
- [x] T078 Implement JWT token expiration handling in frontend (401 → redirect to login)

### Performance & Optimization

- [x] T079 [P] Add database indexes for conversation and message queries in backend/src/models/
- [x] T080 [P] Verify conversation history retrieval is limited to 50 messages or 30 days
- [x] T081 Test chat endpoint performance with 50+ message conversation history

### Documentation & Validation

- [x] T082 [P] Update CLAUDE.md with Phase III context (AI agent rules, MCP constraints)
- [x] T083 [P] Verify all functional requirements (FR-001 through FR-050) are implemented
- [x] T084 Validate spec → plan → tasks alignment (no orphaned logic, no duplicated responsibilities)
- [x] T085 Run quickstart.md validation: install dependencies, start servers, test chat endpoint
- [x] T086 Final review: all todo operations work via chat, no manual coding performed, clear agent/tool separation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P2 → P2 → P3)
- **Frontend (Phase 8)**: Depends on at least one user story being complete (recommend US1 + US2)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories (but builds on US1 conceptually)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories (conversation persistence is foundational)

### Within Each Phase

- **Setup**: All tasks can run in parallel (marked [P])
- **Foundational**: Database models → Services → MCP tools → AI agent → Chat API (some parallelism within each group)
- **User Stories**: Each story is independent; tasks within a story are sequential (verify → implement → test)
- **Frontend**: Most tasks can run in parallel (marked [P]), then integration tasks
- **Polish**: Most tasks can run in parallel (marked [P])

### Parallel Opportunities

- **Phase 1 (Setup)**: All 7 tasks can run in parallel
- **Phase 2 (Foundational)**:
  - T008, T009 (models) in parallel
  - T011, T012 (services) in parallel after models
  - T014-T018 (MCP tools) in parallel after MCP server (T013)
- **Phase 3-7 (User Stories)**: All 5 user stories can be worked on in parallel by different developers after Phase 2
- **Phase 8 (Frontend)**: T062-T065 can run in parallel
- **Phase 9 (Polish)**: T074-T076, T079-T080, T082-T083 can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# After T001-T007 (Setup) complete, launch foundational tasks:

# Parallel group 1: Database models
Task T008: "Create Conversation model in backend/src/models/conversation.py"
Task T009: "Create Message model in backend/src/models/message.py"

# Sequential: Import models
Task T010: "Import models in backend/src/main.py"

# Parallel group 2: Services
Task T011: "Implement conversation_service.py"
Task T012: "Implement message_service.py"

# Sequential: MCP server
Task T013: "Initialize MCP server"

# Parallel group 3: MCP tools
Task T014: "Implement add_task MCP tool"
Task T015: "Implement list_tasks MCP tool"
Task T016: "Implement update_task MCP tool"
Task T017: "Implement complete_task MCP tool"
Task T018: "Implement delete_task MCP tool"

# Sequential: Register tools, then AI agent, then chat API
Task T019 → T020 → T021 → T022 → T023 → T024 → T025 → T026 → T027
```

---

## Parallel Example: User Stories (After Foundational Complete)

```bash
# All user stories can start in parallel:

Developer A: Phase 3 (User Story 1) - Tasks T028-T032
Developer B: Phase 4 (User Story 2) - Tasks T033-T041
Developer C: Phase 5 (User Story 3) - Tasks T042-T047
Developer D: Phase 6 (User Story 4) - Tasks T048-T054
Developer E: Phase 7 (User Story 5) - Tasks T055-T061

# Each developer works independently on their story
# Stories integrate seamlessly because they share the foundational layer
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T027) - CRITICAL
3. Complete Phase 3: User Story 1 (T028-T032) - Add tasks via chat
4. Complete Phase 4: User Story 2 (T033-T041) - List and complete tasks via chat
5. Complete Phase 8: Frontend (T062-T073) - Chat UI
6. **STOP and VALIDATE**: Test US1 + US2 independently via frontend
7. Deploy/demo MVP (basic task management via chat)

**MVP Scope**: 27 foundational tasks + 5 US1 tasks + 9 US2 tasks + 12 frontend tasks = 53 tasks

### Incremental Delivery

1. **Foundation** (Phase 1-2): Setup + Foundational → Backend ready (27 tasks)
2. **MVP** (Phase 3-4 + Phase 8): Add US1 + US2 + Frontend → Basic chat working (26 tasks)
3. **Enhanced** (Phase 5-6): Add US3 + US4 → Full CRUD via chat (16 tasks)
4. **Complete** (Phase 7): Add US5 → Conversation persistence (7 tasks)
5. **Production** (Phase 9): Polish + validation → Production-ready (13 tasks)

Total: 89 tasks

### Parallel Team Strategy

With 3 developers after foundational phase:

1. **Week 1**: All developers complete Setup + Foundational together (27 tasks)
2. **Week 2**:
   - Developer A: User Story 1 + User Story 2 (14 tasks)
   - Developer B: User Story 3 + User Story 4 (16 tasks)
   - Developer C: User Story 5 + Frontend (19 tasks)
3. **Week 3**: All developers work on Polish together (13 tasks)

---

## Task Summary

**Total Tasks**: 89

**By Phase**:
- Phase 1 (Setup): 7 tasks
- Phase 2 (Foundational): 20 tasks
- Phase 3 (US1 - P1): 5 tasks
- Phase 4 (US2 - P1): 9 tasks
- Phase 5 (US3 - P2): 6 tasks
- Phase 6 (US4 - P2): 7 tasks
- Phase 7 (US5 - P3): 7 tasks
- Phase 8 (Frontend): 12 tasks
- Phase 9 (Polish): 13 tasks

**By Priority**:
- P1 (Critical): 41 tasks (Setup + Foundational + US1 + US2 + Frontend core)
- P2 (Important): 13 tasks (US3 + US4)
- P3 (Nice-to-have): 7 tasks (US5)
- Polish: 13 tasks

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel within their phase

**Independent User Stories**: All 5 user stories are independently testable after foundational phase

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Tests are not included (not explicitly requested in specification)
- MCP SDK may need manual implementation if official SDK is unavailable (see research.md)
- Frontend uses @chatscope/chat-ui-kit-react (not "OpenAI ChatKit" which doesn't exist - see research.md)
