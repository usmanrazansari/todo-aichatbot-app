# Quickstart Guide: AI-Powered Chatbot via MCP

**Feature**: 001-ai-chatbot-mcp
**Date**: 2026-02-08
**Audience**: Developers implementing Phase III

## Overview

This guide provides step-by-step instructions for setting up, developing, and testing the AI-powered chatbot feature. Follow this guide to get the development environment running and understand the implementation workflow.

## Prerequisites

### Required Software

- **Python 3.11+**: Backend runtime
- **Node.js 18+**: Frontend runtime
- **npm or yarn**: Package manager
- **Git**: Version control
- **SQLite**: Database (included with Python)

### Required Accounts & API Keys

- **OpenAI API Key**: For AI agent functionality
  - Sign up at https://platform.openai.com/
  - Create API key in dashboard
  - Set environment variable: `OPENAI_API_KEY=sk-...`

### Existing Phase II Setup

This feature extends Phase II. Ensure Phase II is working:
- Backend running on `http://localhost:8000`
- Frontend running on `http://localhost:3000`
- Better Auth configured and working
- Database initialized with Task table

## Installation

### 1. Backend Dependencies

Install new Python packages for Phase III:

```bash
cd backend

# Install OpenAI SDK (for AI agent)
pip install openai>=1.0.0

# Install MCP SDK (if available)
pip install mcp
# OR if not available, we'll implement MCP protocol manually

# Install additional dependencies
pip install python-dotenv  # For environment variables (if not already installed)
```

Update `backend/requirements.txt`:

```txt
# Existing Phase II dependencies
fastapi==0.104.1
uvicorn==0.24.0
sqlmodel==0.0.14
pyjwt==2.8.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Phase III: AI & MCP
openai>=1.0.0
mcp>=0.1.0  # Adjust version based on actual package
```

### 2. Frontend Dependencies

Install new npm packages for Phase III:

```bash
cd frontend

# Install chat UI library
npm install @chatscope/chat-ui-kit-react @chatscope/chat-ui-kit-styles

# Install additional dependencies if needed
npm install axios  # If not already installed
```

Update `frontend/package.json` (should be automatic after npm install).

### 3. Environment Variables

Create or update `.env` files:

**Backend** (`backend/.env`):

```env
# Existing Phase II variables
DATABASE_URL=sqlite:///./todo_app.db
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256

# Phase III: OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo for lower cost

# Phase III: MCP (if needed)
MCP_SERVER_PORT=8001  # Optional: separate port for MCP server
```

**Frontend** (`frontend/.env.local`):

```env
# Existing Phase II variables
NEXT_PUBLIC_API_URL=http://localhost:8000

# Phase III: No additional frontend env vars needed
```

### 4. Database Migration

The database will auto-migrate on startup (SQLModel creates new tables automatically).

To manually verify:

```bash
cd backend

# Start Python shell
python

# Run migration
>>> from src.db.database import engine
>>> from src.models.conversation import Conversation
>>> from src.models.message import Message
>>> from sqlmodel import SQLModel
>>> SQLModel.metadata.create_all(engine)
>>> exit()
```

Verify tables exist:

```bash
sqlite3 backend/todo_app.db

sqlite> .tables
# Should show: conversation, message, task

sqlite> .schema conversation
sqlite> .schema message
sqlite> .quit
```

## Project Structure

After implementation, the project structure will be:

```
backend/src/
├── models/
│   ├── task.py              # Existing
│   ├── conversation.py      # NEW
│   └── message.py           # NEW
├── services/
│   ├── task_service.py      # Existing
│   ├── conversation_service.py  # NEW
│   └── message_service.py   # NEW
├── api/
│   ├── task_routes.py       # Existing
│   ├── auth_routes.py       # Existing
│   └── chat_routes.py       # NEW
├── ai/
│   ├── agent.py             # NEW: OpenAI agent
│   └── prompts.py           # NEW: System prompts
├── mcp/
│   ├── server.py            # NEW: MCP server
│   └── tools/               # NEW: MCP tools
│       ├── add_task.py
│       ├── list_tasks.py
│       ├── update_task.py
│       ├── complete_task.py
│       └── delete_task.py
└── main.py                  # Updated: add chat routes

frontend/src/
├── pages/
│   ├── dashboard.tsx        # Existing
│   ├── login.tsx            # Existing
│   ├── register.tsx         # Existing
│   └── chat.tsx             # NEW
├── components/
│   ├── TaskList.tsx         # Existing
│   ├── TaskForm.tsx         # Existing
│   └── ChatInterface.tsx    # NEW
└── services/
    ├── api.ts               # Existing
    └── chatApi.ts           # NEW
```

## Development Workflow

### Step 1: Implement Database Models

Start with the foundation:

```bash
# Create conversation model
touch backend/src/models/conversation.py

# Create message model
touch backend/src/models/message.py
```

Refer to `specs/001-ai-chatbot-mcp/data-model.md` for schema details.

### Step 2: Implement Service Layer

Create CRUD operations:

```bash
# Create conversation service
touch backend/src/services/conversation_service.py

# Create message service
touch backend/src/services/message_service.py
```

### Step 3: Implement MCP Tools

Create MCP server and tools:

```bash
# Create MCP directory structure
mkdir -p backend/src/mcp/tools

# Create MCP server
touch backend/src/mcp/server.py

# Create individual tools
touch backend/src/mcp/tools/add_task.py
touch backend/src/mcp/tools/list_tasks.py
touch backend/src/mcp/tools/update_task.py
touch backend/src/mcp/tools/complete_task.py
touch backend/src/mcp/tools/delete_task.py
```

Refer to `specs/001-ai-chatbot-mcp/contracts/mcp-tools.json` for tool schemas.

### Step 4: Implement AI Agent

Create AI agent with OpenAI SDK:

```bash
# Create AI directory
mkdir -p backend/src/ai

# Create agent
touch backend/src/ai/agent.py

# Create prompts
touch backend/src/ai/prompts.py
```

### Step 5: Implement Chat API

Create chat endpoint:

```bash
# Create chat routes
touch backend/src/api/chat_routes.py
```

Refer to `specs/001-ai-chatbot-mcp/contracts/chat-api.yaml` for API spec.

### Step 6: Implement Frontend

Create chat UI:

```bash
# Create chat page
touch frontend/src/pages/chat.tsx

# Create chat component
touch frontend/src/components/ChatInterface.tsx

# Create chat API client
touch frontend/src/services/chatApi.ts

# Create chat types
touch frontend/src/types/chat.ts
```

## Running the Application

### Start Backend

```bash
cd backend

# Activate virtual environment (if using)
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Start FastAPI server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`

### Start Frontend

```bash
cd frontend

# Start Next.js dev server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### Verify Setup

1. **Backend Health Check**:
   ```bash
   curl http://localhost:8000/
   # Should return: {"message": "Todo Application API is running!"}
   ```

2. **Database Tables**:
   ```bash
   sqlite3 backend/todo_app.db ".tables"
   # Should show: conversation, message, task
   ```

3. **Frontend**:
   - Open `http://localhost:3000` in browser
   - Should see existing Phase II UI

## Testing

### Unit Tests

Test individual components:

```bash
cd backend

# Test MCP tools
pytest tests/unit/test_mcp_tools.py -v

# Test conversation service
pytest tests/unit/test_conversation_service.py -v

# Test message service
pytest tests/unit/test_message_service.py -v
```

### Integration Tests

Test API endpoints:

```bash
cd backend

# Test chat endpoint
pytest tests/integration/test_chat_endpoint.py -v

# Test agent-MCP flow
pytest tests/integration/test_agent_mcp_flow.py -v
```

### Frontend Tests

Test React components:

```bash
cd frontend

# Test chat interface
npm test -- ChatInterface.test.tsx
```

### Manual Testing

#### Test Chat Endpoint (curl)

```bash
# 1. Login to get JWT token
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}' \
  | jq -r '.access_token')

# 2. Send chat message (new conversation)
curl -X POST http://localhost:8000/api/USER_ID/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Add buy groceries to my tasks"}' \
  | jq

# 3. Send follow-up message (continue conversation)
curl -X POST http://localhost:8000/api/USER_ID/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is on my list?","conversation_id":"CONVERSATION_ID"}' \
  | jq
```

#### Test Chat UI (Browser)

1. Navigate to `http://localhost:3000/chat`
2. Login if not authenticated
3. Type: "Add buy groceries to my tasks"
4. Verify: Task is created and assistant confirms
5. Type: "What's on my list?"
6. Verify: Assistant lists tasks
7. Type: "Mark buy groceries as complete"
8. Verify: Task is marked complete

## Debugging

### Common Issues

#### Issue: OpenAI API Error

**Symptom**: `openai.APIError: Invalid API key`

**Solution**:
- Verify `OPENAI_API_KEY` is set in `backend/.env`
- Check API key is valid at https://platform.openai.com/
- Restart backend server after updating `.env`

#### Issue: MCP SDK Not Found

**Symptom**: `ModuleNotFoundError: No module named 'mcp'`

**Solution**:
- Check if MCP SDK is available: `pip list | grep mcp`
- If not available, implement MCP protocol manually (fallback plan)
- See `specs/001-ai-chatbot-mcp/research.md` for alternatives

#### Issue: Database Tables Not Created

**Symptom**: `sqlite3.OperationalError: no such table: conversation`

**Solution**:
- Ensure models are imported in `main.py`:
  ```python
  from src.models.conversation import Conversation
  from src.models.message import Message
  ```
- Restart backend server (tables created on startup)
- Manually run migration (see Installation step 4)

#### Issue: JWT Token Expired

**Symptom**: `401 Unauthorized` on chat endpoint

**Solution**:
- Login again to get fresh token
- Check JWT expiration time in `backend/src/utils/jwt_handler.py`
- Frontend should handle token refresh automatically

### Logging

Enable debug logging:

**Backend** (`backend/src/main.py`):

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**View Logs**:
- Backend logs appear in terminal where `uvicorn` is running
- Frontend logs appear in browser console (F12)

### Database Inspection

Inspect database contents:

```bash
sqlite3 backend/todo_app.db

# View conversations
sqlite> SELECT * FROM conversation;

# View messages
sqlite> SELECT * FROM message ORDER BY created_at;

# View tasks
sqlite> SELECT * FROM task;

# Count messages per conversation
sqlite> SELECT conversation_id, COUNT(*) as message_count
        FROM message
        GROUP BY conversation_id;
```

## Performance Optimization

### Database Indexes

Verify indexes are created:

```bash
sqlite3 backend/todo_app.db

sqlite> .indexes conversation
sqlite> .indexes message
```

If missing, create manually:

```sql
CREATE INDEX idx_conversation_user ON conversation(user_id);
CREATE INDEX idx_conversation_user_updated ON conversation(user_id, updated_at DESC);
CREATE INDEX idx_message_conversation ON message(conversation_id);
CREATE INDEX idx_message_user ON message(user_id);
CREATE INDEX idx_message_conversation_created ON message(conversation_id, created_at DESC);
```

### OpenAI API Optimization

Reduce API costs:
- Use `gpt-3.5-turbo` instead of `gpt-4` for development
- Limit conversation history to 25 messages (instead of 50)
- Cache system prompts

### Frontend Optimization

Improve UI responsiveness:
- Show typing indicator while waiting for AI response
- Debounce user input (prevent rapid-fire requests)
- Cache conversation history in localStorage

## Next Steps

After completing the quickstart setup:

1. **Review Specification**: Read `specs/001-ai-chatbot-mcp/spec.md`
2. **Review Plan**: Read `specs/001-ai-chatbot-mcp/plan.md`
3. **Review Research**: Read `specs/001-ai-chatbot-mcp/research.md`
4. **Review Data Model**: Read `specs/001-ai-chatbot-mcp/data-model.md`
5. **Review Contracts**: Read API and tool schemas in `specs/001-ai-chatbot-mcp/contracts/`
6. **Generate Tasks**: Run `/sp.tasks` to create implementation tasks
7. **Start Implementation**: Follow tasks in order

## Resources

### Documentation

- **OpenAI API**: https://platform.openai.com/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLModel**: https://sqlmodel.tiangolo.com/
- **Next.js**: https://nextjs.org/docs
- **Chat UI Kit**: https://chatscope.io/storybook/react/

### Project Files

- Specification: `specs/001-ai-chatbot-mcp/spec.md`
- Implementation Plan: `specs/001-ai-chatbot-mcp/plan.md`
- Research: `specs/001-ai-chatbot-mcp/research.md`
- Data Model: `specs/001-ai-chatbot-mcp/data-model.md`
- API Contract: `specs/001-ai-chatbot-mcp/contracts/chat-api.yaml`
- MCP Tools: `specs/001-ai-chatbot-mcp/contracts/mcp-tools.json`

### Support

For issues or questions:
- Check existing Phase II implementation for patterns
- Review research document for technical decisions
- Consult API contracts for endpoint specifications
- Run tests to verify functionality

## Summary

This quickstart guide covers:
- ✅ Prerequisites and dependencies
- ✅ Installation steps
- ✅ Project structure
- ✅ Development workflow
- ✅ Running and testing
- ✅ Debugging common issues
- ✅ Performance optimization
- ✅ Next steps and resources

Follow this guide to set up the development environment and begin implementing Phase III: AI-Powered Chatbot via MCP.
