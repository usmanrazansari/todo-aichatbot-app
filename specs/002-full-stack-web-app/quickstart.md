# Quickstart Guide: Todo Application – Phase II (Full-Stack Web Application)

## Prerequisites

- Node.js 18+ (for frontend development)
- Python 3.13+ (for backend development)
- Poetry (for Python dependency management)
- npm or yarn (for JavaScript dependency management)
- Neon PostgreSQL account (for database)

## Environment Setup

### 1. Clone and Initialize the Repository
```bash
# Clone the repository
git clone [repository-url]
cd [repository-name]

# Install backend dependencies
cd backend
pip install poetry
poetry install

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Configure Environment Variables

Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
BETTER_AUTH_SECRET=your-super-secret-jwt-signing-key-here
```

Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 3. Set Up the Database
```bash
# From the backend directory
cd backend
poetry run python -m src.db.database  # Or use Alembic for migrations
```

## Running the Application

### 1. Start the Backend
```bash
cd backend
poetry run uvicorn src.main:app --reload --port=8000
```

### 2. Start the Frontend
```bash
cd frontend
npm run dev
```

The application will be available at http://localhost:3000

## Project Structure Overview

### Backend Structure
```
backend/
├── src/
│   ├── models/         # Data models (SQLModel)
│   ├── services/       # Business logic
│   ├── api/            # API route handlers
│   ├── db/             # Database connection and utilities
│   ├── utils/          # Helper functions
│   └── main.py         # FastAPI app entry point
├── tests/              # Backend tests
├── requirements.txt    # Python dependencies
└── pyproject.toml      # Poetry configuration
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/     # Reusable React components
│   ├── pages/          # Next.js pages
│   ├── services/       # API clients and auth utilities
│   ├── types/          # TypeScript type definitions
│   ├── styles/         # Global styles
│   └── utils/          # Utility functions
├── public/             # Static assets
├── package.json        # JavaScript dependencies
└── next.config.js      # Next.js configuration
```

## Key Development Commands

### Backend Commands
```bash
# Run the backend server
poetry run uvicorn src.main:app --reload --port=8000

# Run backend tests
poetry run pytest

# Format backend code
poetry run black src/
poetry run isort src/
```

### Frontend Commands
```bash
# Run the frontend development server
npm run dev

# Build the frontend for production
npm run build

# Run frontend tests
npm run test

# Format frontend code
npm run format
npm run lint
```

## Authentication Flow

1. User registers/login via Better Auth forms
2. Better Auth issues JWT token upon successful authentication
3. Frontend stores JWT token in secure storage
4. All API requests include JWT token in Authorization header
5. Backend validates JWT token and extracts user identity
6. Backend enforces user ownership of tasks

## Making API Requests

The frontend service handles API calls with proper authentication:

```typescript
import { apiClient } from '@/services/api';

// Example: Fetch user's tasks
const tasks = await apiClient.get(`/api/${userId}/tasks`);

// Example: Create a new task
const newTask = await apiClient.post(`/api/${userId}/tasks`, {
  title: 'New task',
  description: 'Task description'
});
```

## Database Models

### Task Model
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Common Development Tasks

### Adding a New API Endpoint
1. Define the endpoint in the appropriate route handler file
2. Create Pydantic models for request/response validation
3. Implement the business logic in a service module
4. Add authentication and authorization checks
5. Add tests for the new functionality

### Adding a New Frontend Component
1. Create the component in the `components/` directory
2. Use TypeScript interfaces for props
3. Implement responsive design with Tailwind CSS
4. Add unit tests for the component
5. Export the component in an index file if needed

## Testing

### Backend Testing
Run all backend tests:
```bash
cd backend
poetry run pytest
```

Run tests with coverage:
```bash
poetry run pytest --cov=src --cov-report=html
```

### Frontend Testing
Run all frontend tests:
```bash
cd frontend
npm run test
```

Run tests in watch mode:
```bash
npm run test:watch
```

## Deployment

### Environment Variables for Production
- `DATABASE_URL`: Production PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Production JWT signing key
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Production frontend URL
- `NEXT_PUBLIC_API_BASE_URL`: Production backend API URL

### Build and Deploy Commands
```bash
# Build frontend for production
cd frontend
npm run build

# Backend typically runs via WSGI server in production
# (gunicorn, uvicorn with process manager, etc.)
```