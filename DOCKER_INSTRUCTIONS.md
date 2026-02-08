# Docker Build and Run Instructions

## Prerequisites
- Docker installed and running
- Docker Compose installed (usually comes with Docker Desktop)

## Option 1: Build and Run with Docker Compose (Recommended)

### Build and start all services:
```bash
docker-compose up --build
```

### Run in detached mode (background):
```bash
docker-compose up -d --build
```

### Stop all services:
```bash
docker-compose down
```

### Stop and remove volumes:
```bash
docker-compose down -v
```

### View logs:
```bash
docker-compose logs -f
```

## Option 2: Build Individual Images

### Build Backend Image:
```bash
cd backend
docker build -t todo-backend:latest .
```

### Build Frontend Image:
```bash
cd frontend
docker build -t todo-frontend:latest .
```

### Run Backend Container:
```bash
docker run -d \
  --name todo-backend \
  -p 8001:8001 \
  -e DATABASE_URL=sqlite:///./data/todo.db \
  -e OPENROUTER_API_KEY=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 \
  -e AI_MODEL=openai/gpt-4o-mini \
  -v todo-data:/app/data \
  todo-backend:latest
```

### Run Frontend Container:
```bash
docker run -d \
  --name todo-frontend \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_BASE_URL=http://localhost:8001 \
  --link todo-backend:backend \
  todo-frontend:latest
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **Backend Health Check**: http://localhost:8001/health

## Useful Docker Commands

### View running containers:
```bash
docker ps
```

### View all containers (including stopped):
```bash
docker ps -a
```

### View logs for a specific container:
```bash
docker logs todo-backend
docker logs todo-frontend
```

### Stop a container:
```bash
docker stop todo-backend
docker stop todo-frontend
```

### Remove a container:
```bash
docker rm todo-backend
docker rm todo-frontend
```

### Remove images:
```bash
docker rmi todo-backend:latest
docker rmi todo-frontend:latest
```

## Troubleshooting

### If port is already in use:
```bash
# Find process using the port
netstat -ano | findstr :3000
netstat -ano | findstr :8001

# Kill the process (Windows)
taskkill /PID <process_id> /F
```

### Rebuild without cache:
```bash
docker-compose build --no-cache
```

### Clean up all Docker resources:
```bash
docker system prune -a
```

## Environment Variables

You can modify environment variables in `docker-compose.yml` or pass them when running individual containers.

### Backend Environment Variables:
- `DATABASE_URL`: Database connection string
- `OPENROUTER_API_KEY`: OpenRouter API key for AI features
- `AI_MODEL`: AI model to use (default: openai/gpt-4o-mini)
- `BETTER_AUTH_SECRET`: Secret key for authentication
- `BETTER_AUTH_URL`: Frontend URL for authentication

### Frontend Environment Variables:
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL
