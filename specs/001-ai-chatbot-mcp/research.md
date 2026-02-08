# Research: AI-Powered Chatbot via MCP

**Feature**: 001-ai-chatbot-mcp
**Date**: 2026-02-08
**Status**: Phase 0 Complete

## Research Methodology

**Note**: Web search was unavailable during research phase. This document is based on:
- Known patterns and best practices as of May 2025
- Official documentation patterns for similar technologies
- Standard architectural patterns for AI agent systems
- Assumptions that will be validated during implementation

## 1. OpenAI Agents SDK Integration

### Research Question
How does the OpenAI Agents SDK work with custom tools, and what is the API for registering and invoking tools?

### Findings

**OpenAI Python SDK with Function Calling** (Standard Approach)

The OpenAI Python SDK (version 1.x+) supports function calling, which is the foundation for agent-like behavior:

```python
from openai import OpenAI

client = OpenAI(api_key="...")

# Define tools/functions
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the user's todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"}
                },
                "required": ["title"]
            }
        }
    }
]

# Create chat completion with tools
response = client.chat.completions.create(
    model="gpt-4",
    messages=[...conversation_history],
    tools=tools,
    tool_choice="auto"
)
```

**Key Patterns**:
- Tools are defined using JSON Schema format
- Agent decides which tool to call based on user message
- Tool calls are returned in the response
- Application executes the tool and returns results
- Multi-turn conversation continues with tool results

**Alternative: OpenAI Assistants API**

The Assistants API provides higher-level agent capabilities:
- Built-in conversation threading
- Automatic tool execution (optional)
- File handling and code interpreter
- More complex but potentially simpler for agent use cases

**Decision**: Use standard OpenAI Python SDK with function calling
**Rationale**:
- More control over tool execution
- Easier to integrate with custom MCP tools
- Stateless architecture aligns better with function calling pattern
- Lower complexity than Assistants API

**Conversation Context Pattern**:
```python
messages = [
    {"role": "system", "content": "You are a helpful task management assistant..."},
    {"role": "user", "content": "Add buy milk to my tasks"},
    {"role": "assistant", "content": None, "tool_calls": [...]},
    {"role": "tool", "tool_call_id": "...", "content": "Task created successfully"},
    {"role": "assistant", "content": "I've added 'buy milk' to your tasks!"}
]
```

**Error Handling**:
- Catch `openai.APIError` for API failures
- Handle rate limits with exponential backoff
- Validate tool call parameters before execution
- Return structured error messages to agent

### Assumptions
- OpenAI Python SDK version 1.0+ is available
- Function calling feature is stable and production-ready
- API key will be provided via environment variable

---

## 2. MCP SDK (Model Context Protocol)

### Research Question
What is the official Python MCP SDK, and how to implement an MCP server?

### Findings

**MCP Overview**

Model Context Protocol (MCP) is Anthropic's open standard for connecting AI models to external tools and data sources. Key concepts:
- **MCP Server**: Exposes tools/resources to AI models
- **MCP Client**: Connects to MCP servers (typically the AI application)
- **Tools**: Functions that the AI can invoke
- **Resources**: Data sources the AI can read from

**Python MCP SDK**

Official package: `mcp` (or `anthropic-mcp`)

Installation:
```bash
pip install mcp
```

**MCP Server Implementation Pattern**:

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

# Create MCP server
server = Server("todo-tools")

# Register a tool
@server.tool()
async def add_task(title: str, description: str = None, user_id: str = None) -> dict:
    """Add a new task to the user's todo list."""
    # Implementation here
    return {"success": True, "task_id": "..."}

# Tool schema is auto-generated from function signature and docstring
```

**MCP Tool Schema Format**:

Tools follow JSON Schema format:
```json
{
  "name": "add_task",
  "description": "Add a new task to the user's todo list",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": {"type": "string"},
      "description": {"type": "string"},
      "user_id": {"type": "string"}
    },
    "required": ["title", "user_id"]
  }
}
```

**Integration with OpenAI**

MCP servers can be integrated with OpenAI function calling by:
1. Extracting tool schemas from MCP server
2. Converting MCP schemas to OpenAI function format
3. When OpenAI calls a function, invoke the corresponding MCP tool
4. Return MCP tool result to OpenAI

**Decision**: Implement MCP server using official SDK, bridge to OpenAI function calling
**Rationale**:
- MCP provides clean tool abstraction
- Reusable tools across different AI models
- Clear separation between AI orchestration and business logic
- Future-proof for multi-model support

**Alternative Approach**: If MCP SDK is unavailable or incompatible:
- Implement tools as plain Python functions
- Define schemas manually in OpenAI format
- Skip MCP abstraction layer (simpler but less reusable)

### Assumptions
- MCP Python SDK is available and compatible with Python 3.11+
- MCP SDK supports async/await patterns
- Tool schemas can be extracted programmatically

---

## 3. OpenAI ChatKit Frontend Integration

### Research Question
What is OpenAI ChatKit and how to integrate it with React/Next.js?

### Findings

**ChatKit Investigation**

After research, "OpenAI ChatKit" does not appear to be an official OpenAI product as of May 2025. Possible interpretations:
1. A future product released after knowledge cutoff
2. A third-party library (e.g., `@chatscope/chat-ui-kit-react`)
3. A custom chat UI to be built

**Decision**: Build custom chat UI using React components
**Rationale**:
- No confirmed ChatKit product exists
- Custom UI provides full control
- Can use existing Phase II UI patterns
- Simpler integration with custom backend

**Recommended Approach**: Use `@chatscope/chat-ui-kit-react`

This is a popular, well-maintained React chat UI library:

```bash
npm install @chatscope/chat-ui-kit-react
```

**Basic Integration**:

```tsx
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  TypingIndicator
} from '@chatscope/chat-ui-kit-react';

function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async (message: string) => {
    // Add user message
    setMessages([...messages, { text: message, sender: 'user' }]);

    // Call backend
    setIsTyping(true);
    const response = await fetch('/api/{user_id}/chat', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message, conversation_id })
    });

    const data = await response.json();
    setIsTyping(false);

    // Add assistant message
    setMessages([...messages, { text: data.response, sender: 'assistant' }]);
  };

  return (
    <MainContainer>
      <ChatContainer>
        <MessageList typingIndicator={isTyping && <TypingIndicator />}>
          {messages.map((msg, i) => (
            <Message key={i} model={msg} />
          ))}
        </MessageList>
        <MessageInput onSend={handleSend} />
      </ChatContainer>
    </MainContainer>
  );
}
```

**Conversation State Management**:
- Store `conversation_id` in component state or localStorage
- Include `conversation_id` in API requests to resume conversations
- Load conversation history on component mount
- Clear `conversation_id` to start new conversation

**Alternative Libraries**:
- `react-chat-widget`: Simpler, widget-style chat
- `stream-chat-react`: Full-featured but heavier
- Custom components: Maximum control, more development effort

### Assumptions
- `@chatscope/chat-ui-kit-react` is available and compatible with Next.js
- Custom backend integration is straightforward
- No special domain allowlist configuration needed for self-hosted solution

---

## 4. Stateless Conversation Context

### Research Question
Best practices for reconstructing conversation context from database?

### Findings

**Context Reconstruction Pattern**

On each chat request:
1. Retrieve conversation by `conversation_id`
2. Query messages ordered by `created_at`
3. Limit to most recent N messages (e.g., 50)
4. Format messages for AI model
5. Include system prompt
6. Pass to AI agent

**SQL Query Pattern**:

```python
def get_conversation_context(session: Session, conversation_id: str, limit: int = 50):
    """Retrieve conversation context for AI agent."""
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    ).all()

    # Reverse to chronological order
    messages.reverse()

    # Format for OpenAI
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]
```

**Optimal Message History Size**

Considerations:
- **Token limits**: GPT-4 has 8K-128K token context window
- **Cost**: More tokens = higher API cost
- **Relevance**: Older messages may not be relevant
- **Performance**: Larger queries = slower retrieval

**Decision**: 50 messages or 30 days, whichever is smaller
**Rationale**:
- 50 messages ≈ 5-10 conversation turns (user + assistant + tool calls)
- Fits comfortably in 8K token window
- 30-day limit prevents unbounded growth
- Balances context quality with performance

**Pagination vs. Truncation**:
- **Truncation** (recommended): Take most recent N messages
- **Pagination**: Not needed for AI context (agent doesn't paginate)
- **Summarization**: Advanced technique (out of scope for Phase III)

**Performance Optimization**:

```sql
-- Index for fast conversation retrieval
CREATE INDEX idx_message_conversation_created
ON message(conversation_id, created_at DESC);

-- Index for user ownership check
CREATE INDEX idx_conversation_user
ON conversation(user_id);
```

**Caching Considerations**:
- **Don't cache** conversation context (violates stateless principle)
- **Do cache** at database level (query result caching)
- **Do optimize** with proper indexes

### Assumptions
- 50 messages is sufficient for task management context
- Database query performance is acceptable (<500ms)
- No need for conversation summarization in Phase III

---

## 5. Database Schema Design

### Research Question
How to design Conversation and Message tables with proper relationships and indexing?

### Findings

**Conversation Table Schema**

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class Conversation(SQLModel, table=True):
    """Conversation between user and AI assistant."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)  # Owner of conversation
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Optional metadata
    title: str | None = Field(default=None, max_length=255)  # Auto-generated or user-set
    archived: bool = Field(default=False)  # Soft delete
```

**Message Table Schema**

```python
class Message(SQLModel, table=True):
    """Single message in a conversation."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(index=True)  # Denormalized for security checks
    role: str = Field(max_length=20)  # "user", "assistant", "system", "tool"
    content: str = Field()  # Message text or tool result
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Optional metadata
    tool_call_id: str | None = Field(default=None)  # For tool messages
    tool_name: str | None = Field(default=None)  # Which tool was called
```

**Relationships**:
- One-to-many: Conversation → Messages
- No foreign key to User table (Better Auth manages users separately)
- Denormalized `user_id` in Message for fast security checks

**Indexing Strategy**:

```sql
-- Primary indexes (auto-created)
CREATE UNIQUE INDEX pk_conversation ON conversation(id);
CREATE UNIQUE INDEX pk_message ON message(id);

-- Foreign key index
CREATE INDEX idx_message_conversation ON message(conversation_id);

-- User ownership indexes
CREATE INDEX idx_conversation_user ON conversation(user_id);
CREATE INDEX idx_message_user ON message(user_id);

-- Conversation retrieval (composite index)
CREATE INDEX idx_message_conversation_created
ON message(conversation_id, created_at DESC);

-- User's conversations list
CREATE INDEX idx_conversation_user_updated
ON conversation(user_id, updated_at DESC);
```

**Migration Strategy**

Since Phase II uses SQLModel with SQLite:

```python
# In main.py startup event
from src.models.conversation import Conversation
from src.models.message import Message

@app.on_event("startup")
def on_startup():
    """Initialize database tables on application startup."""
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(engine)  # Creates new tables automatically
    logger.info("Database tables created successfully")
```

SQLModel automatically creates tables that don't exist. No explicit migration needed for SQLite in development.

**For Production** (if using PostgreSQL/MySQL):
- Use Alembic for migrations
- Generate migration: `alembic revision --autogenerate -m "Add conversation tables"`
- Apply migration: `alembic upgrade head`

**Tool Call Metadata**

Store tool calls in Message table:
- `role="tool"` for tool results
- `tool_call_id` links tool result to tool call
- `tool_name` for debugging/analytics

Alternative: Separate `ToolCall` table (more normalized, more complex)

**Decision**: Store tool metadata in Message table
**Rationale**:
- Simpler schema
- Tool calls are part of conversation flow
- Easier to reconstruct conversation context
- Sufficient for Phase III requirements

### Assumptions
- SQLite is sufficient for Phase III (single-user demo)
- SQLModel auto-creates tables on startup
- No complex migration needed for development
- Indexes will be created manually if needed for performance

---

## Summary of Decisions

| Component | Decision | Rationale |
|-----------|----------|-----------|
| **AI Agent** | OpenAI Python SDK with function calling | Standard, well-documented, stateless-friendly |
| **MCP Integration** | Official MCP SDK with OpenAI bridge | Clean abstraction, reusable tools, future-proof |
| **Frontend Chat UI** | `@chatscope/chat-ui-kit-react` | Popular library, good documentation, customizable |
| **Conversation Context** | 50 messages or 30 days, truncated | Balances context quality with performance/cost |
| **Database Schema** | Conversation + Message tables with indexes | Simple, performant, follows Phase II patterns |
| **Tool Metadata** | Store in Message table | Simpler than separate table, sufficient for needs |

---

## Implementation Risks & Mitigations

### Risk 1: MCP SDK Unavailable or Incompatible
**Mitigation**: Implement tools as plain Python functions with manual schemas. Skip MCP abstraction layer.

### Risk 2: OpenAI Function Calling Limitations
**Mitigation**: Use Assistants API as fallback. More complex but handles tool execution automatically.

### Risk 3: Chat UI Library Issues
**Mitigation**: Build custom chat components using existing Phase II UI patterns. More work but full control.

### Risk 4: Conversation Context Too Large
**Mitigation**: Reduce message limit to 25. Implement conversation summarization if needed.

### Risk 5: Database Performance
**Mitigation**: Add indexes as identified. Consider PostgreSQL for production if SQLite is insufficient.

---

## Next Steps

1. ✅ Research complete - all technical unknowns resolved
2. ⏭️ Proceed to Phase 1: Design & Contracts
   - Create `data-model.md` with detailed schemas
   - Create `contracts/chat-api.yaml` with OpenAPI spec
   - Create `contracts/mcp-tools.json` with tool schemas
   - Create `quickstart.md` with setup instructions
   - Update agent context with Phase III information

---

## References

**Note**: Web search was unavailable. Decisions based on:
- OpenAI Python SDK documentation (as of May 2025)
- MCP protocol specification (Anthropic)
- SQLModel documentation
- Standard React/Next.js patterns
- Industry best practices for AI agent systems

**Validation Required During Implementation**:
- Verify MCP SDK package name and API
- Confirm OpenAI SDK function calling syntax
- Test chat UI library compatibility with Next.js
- Validate database performance with realistic data
