# Todo App with AI Chatbot

A full-stack Todo application with an AI-powered chatbot assistant, featuring modern web technologies, Docker containerization, and Kubernetes deployment.

## Features

### Core Functionality
- ✅ User authentication (register/login with JWT)
- ✅ Create, read, update, and delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Responsive dashboard UI with Tailwind CSS
- ✅ Real-time task management

### AI-Powered Chatbot
- 🤖 Natural language task management via AI assistant
- 💬 Conversational interface powered by OpenAI GPT-4
- 🔧 MCP (Model Context Protocol) integration for tool calling
- 📝 Persistent conversation history
- 🎯 Context-aware responses with up to 50 messages history

### Deployment Options
- 🐳 Docker Compose for local development
- ☸️ Kubernetes manifests for production deployment
- 🔄 Health checks and container orchestration
- 📦 Multi-stage Docker builds for optimized images

## Tech Stack

### Frontend
- **Framework:** Next.js 16 with React 19
- **Styling:** Tailwind CSS
- **Language:** TypeScript
- **API Client:** Axios + Fetch API

### Backend
- **Framework:** FastAPI (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** JWT tokens with Better Auth
- **AI Integration:** OpenAI API (GPT-4)
- **MCP Server:** Custom implementation for tool calling

### DevOps
- **Containerization:** Docker & Docker Compose
- **Orchestration:** Kubernetes (minikube)
- **Reverse Proxy:** Nginx (in Kubernetes)

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key (for AI chatbot feature)

### Running with Docker Compose

1. Clone the repository:
```bash
git clone https://github.com/yourusername/todo-app-ai-chatbot.git
cd todo-app-ai-chatbot
```

2. Create a `.env` file in the `backend` directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

3. Start the application:
```bash
docker-compose up -d
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Documentation: http://localhost:8001/docs

### Running with Kubernetes

1. Start minikube:
```bash
minikube start
```

2. Load Docker images into minikube:
```bash
docker save todo-backend:latest | docker exec -i minikube docker load
docker save todo-frontend:latest | docker exec -i minikube docker load
```

3. Apply Kubernetes manifests:
```bash
kubectl apply -f k8s-manifests/
```

4. Access via port forwarding:
```bash
kubectl port-forward svc/todo-frontend 3001:3000
```

Then open: http://localhost:3001

## Project Structure

```
.
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── ai/             # AI agent and prompts
│   │   ├── api/            # API routes
│   │   ├── mcp/            # MCP server and tools
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Next.js pages
│   │   ├── services/      # API clients
│   │   └── types/         # TypeScript types
│   ├── Dockerfile
│   └── package.json
├── k8s-manifests/         # Kubernetes deployment files
├── docker-compose.yml     # Docker Compose configuration
└── README.md
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Tasks
- `GET /api/{user_id}/tasks` - Get all tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{task_id}` - Get task by ID
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle completion

### Chat
- `POST /api/{user_id}/chat` - Send message to AI chatbot
- `GET /api/{user_id}/conversations` - Get conversation history

## AI Chatbot Capabilities

The AI assistant can help you manage tasks through natural language:

**Examples:**
- "Add a task to buy groceries"
- "Show me all my tasks"
- "Mark the first task as complete"
- "Update task 3 to 'Buy milk and eggs'"
- "Delete the completed tasks"

The chatbot uses OpenAI's function calling feature to interact with the task management system through MCP tools.

## Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8001
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=sqlite:///./todo.db
JWT_SECRET=your_jwt_secret
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
```

## Architecture Highlights

### Stateless AI Agent
- AI agent doesn't maintain state between requests
- Conversation history loaded from database for each request
- Up to 50 messages or 30 days of history per conversation

### MCP Integration
- Custom MCP server implementation (SDK not available at development time)
- Tool registry with JSON Schema validation
- Automatic tool invocation based on AI responses

### Security
- JWT-based authentication
- User-scoped data isolation
- Environment-based secrets management
- No sensitive data in logs

## Documentation

- [Docker Instructions](DOCKER_INSTRUCTIONS.md) - Detailed Docker setup guide
- [Phase III Context](CLAUDE.md) - AI chatbot implementation details
- [Prompt History](history/prompts/) - Development session records

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Built with Claude Code (Opus 4.6) using Spec-Driven Development methodology.
