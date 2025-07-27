# AI Chatbot Web Application

A modern, full-stack web application featuring an AI chatbot interface with database management capabilities. Built with React frontend and **Python FastAPI backend using OpenAI's Agents SDK** with streaming responses, containerized with Docker for easy deployment.

## 🆕 NEW: Docker Development Environment

This application now features a **complete Docker development environment** with:
- **Python Virtual Environment** inside containers
- **VS Code Remote Debugging** support
- **Hot Reload** for both frontend and backend
- **Isolated Development** with proper dependency management

## Features

- 🔐 **User Authentication** - Secure login/registration system with JWT tokens
- 💬 **AI Chat Interface** - Interactive chatbot with **real-time streaming responses**
- 🤖 **OpenAI Agents SDK** - Advanced AI capabilities with contextual understanding
- 📊 **Data Management** - Real-time database table view with search and filtering
- 🎨 **Modern UI** - Commonwealth Bank inspired design with yellow and black
- 🐳 **Docker Ready** - Complete development and production containers
- 🔧 **Debug Support** - VS Code debugging with Docker containers
- 📱 **Mobile Friendly** - Responsive design for all device sizes
- ⚡ **Real-time Streaming** - Server-Sent Events for live AI responses

## Architecture

- **Frontend**: React 18 with modern hooks and streaming support
- **Backend**: Python FastAPI with OpenAI Agents SDK integration
- **AI**: OpenAI GPT-4 with streaming responses and context awareness
- **Database**: SQLite for lightweight, embedded storage  
- **Layout**: 80% data table view, 20% chat interface (responsive)
- **Containerization**: Docker with multi-stage builds and virtual environments

## Quick Start

### Prerequisites

- Docker and Docker Compose
- VS Code (recommended for debugging)
- OpenAI API Key (optional - uses mock responses without it)

### Option 1: Docker Development (Recommended)

1. **Clone Repository**
   ```bash
   git clone <your-repo-url>
   cd Banksie
   ```

2. **Set Environment Variables**
   ```bash
   # Optional: Add your OpenAI API key
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   ```

3. **Start Development Environment**
   ```bash
   # Start both Python backend and React frontend in development mode
   docker-compose -f docker-compose.python.yml --profile dev up --build
   ```

4. **Access the Application**
   - **React Frontend**: http://localhost:3000
   - **Python Backend**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Database Admin**: http://localhost:8080 (Adminer)

5. **Login**
   - Username: `admin`
   - Password: `admin123`

### Option 2: Local Development Setup

1. **Setup Python Backend**
   ```bash
   cd python-backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python start.py
   ```

2. **Setup React Frontend**
   ```bash
   cd client
   npm install
   npm start
   ```

## 🐳 Docker Development Features

### **Virtual Environment Inside Container**
- Each container has its own isolated Python virtual environment
- Dependencies are properly managed and cached
- No conflicts with host system Python

### **Development vs Production**
- **Development**: Hot reload, debugging, development tools
- **Production**: Optimized builds, minimal images, production settings

### **Available Profiles**
```bash
# Development mode (hot reload, debugging)
docker-compose -f docker-compose.python.yml --profile dev up

# Production mode (optimized builds)
docker-compose -f docker-compose.python.yml --profile production up
```

## 🔧 VS Code Debugging

### **Docker Remote Debugging**

1. **Start Development Container**
   ```bash
   docker-compose -f docker-compose.python.yml --profile dev up -d
   ```

2. **Attach Debugger in VS Code**
   - Press `F5` → Select **"Debug Python Backend (Docker)"**
   - Set breakpoints in your Python code
   - Debug runs inside the Docker container!

3. **Available Debug Configurations**:
   - `Debug Python Backend (Local)` - Local Python debugging
   - `Debug Python Backend (Docker)` - Remote Docker debugging
   - `Debug Python Backend (Docker - Wait)` - Wait for debugger attachment
   - `Debug React Frontend` - React app debugging
   - `Debug Full Stack (Docker)` - Both frontend and backend

### **Debug Features**
- **Breakpoints** work in Docker containers
- **Variable inspection** and call stack
- **Hot reload** with code changes
- **Path mapping** between host and container

## 🛠️ Available VS Code Tasks

Access via `Ctrl+Shift+P` → "Tasks: Run Task":

- **Start Full Stack (Docker Dev)** - Complete development environment
- **Start Python Backend Docker Dev** - Backend only
- **Start React Frontend** - Frontend only
- **Stop Docker Services** - Stop all containers
- **View Docker Logs** - Monitor container logs
- **Run Tests (Python)** - Execute Python tests
- **Format Python Code** - Auto-format with Black

## Project Structure

```
ai-chatbot-webapp/
├── python-backend/              # Python FastAPI backend
│   ├── main.py                 # FastAPI app with OpenAI integration
│   ├── start.py                # Standard startup script
│   ├── start-debug.py          # Debug startup with debugpy
│   ├── requirements.txt        # Production dependencies
│   ├── requirements.dev.txt    # Development dependencies
│   ├── Dockerfile              # Production container
│   ├── Dockerfile.dev          # Development container
│   └── .env                    # Environment variables
├── client/                     # React frontend
│   ├── src/components/         # React components with streaming
│   ├── Dockerfile              # Production container
│   ├── Dockerfile.dev          # Development container
│   └── package.json           # Updated proxy for Python backend
├── .vscode/                    # VS Code configuration
│   ├── launch.json            # Debug configurations
│   └── tasks.json             # Development tasks
├── docker-compose.python.yml   # Docker development setup
└── README.md
```

## 🤖 OpenAI Integration

### Setting up OpenAI API

1. **Get API Key**: Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Set Environment Variable**:
   ```bash
   # Create .env file in project root
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   ```
3. **Without API Key**: The app uses intelligent mock responses

### AI Agent Features

- **Contextual Understanding**: AI knows about your data structure
- **Streaming Responses**: Real-time message generation
- **Data Analysis**: Can analyze and discuss your business data
- **Professional Tone**: Tailored for business data management

## API Endpoints (Python Backend)

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - User registration

### Data Management
- `GET /api/data` - Fetch table data (authenticated)

### Chat (Streaming)
- `GET /api/chat/history` - Get chat history (authenticated)
- `POST /api/chat/stream` - **Stream AI response** (Server-Sent Events)
- `WS /ws/chat/{user_id}` - WebSocket chat (alternative)

### Health & Docs
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger)

## Environment Configuration

### Docker Environment Variables

```yaml
# Development
environment:
  - DEBUG=True
  - DEBUG_PORT=5678
  - DEBUG_WAIT=False
  - OPENAI_API_KEY=${OPENAI_API_KEY}
  - JWT_SECRET=dev-secret-key
  - PYTHONUNBUFFERED=1
  - PYTHONDONTWRITEBYTECODE=1
```

### Local Development (.env)

```env
# Server Configuration
PORT=8000
DEBUG=True
HOST=0.0.0.0

# Debug Configuration
DEBUG_PORT=5678
DEBUG_WAIT=False

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Security
JWT_SECRET=dev-secret-key
```

## Development Workflow

### **Typical Development Session**

1. **Start Environment**
   ```bash
   docker-compose -f docker-compose.python.yml --profile dev up -d
   ```

2. **Open VS Code**
   ```bash
   code .
   ```

3. **Start Debugging**
   - Press `F5` → Select "Debug Full Stack (Docker)"
   - Set breakpoints in Python code
   - Make changes and see hot reload

4. **View Logs**
   ```bash
   docker-compose -f docker-compose.python.yml logs -f
   ```

5. **Stop Environment**
   ```bash
   docker-compose -f docker-compose.python.yml down
   ```

### **Container Management**

```bash
# View running containers
docker ps

# Access container shell
docker exec -it banksie-ai-chatbot-python-dev-1 bash

# View container logs
docker logs banksie-ai-chatbot-python-dev-1

# Rebuild containers
docker-compose -f docker-compose.python.yml --profile dev up --build
```

## Production Deployment

### Docker Production

```bash
# Set your OpenAI API key
export OPENAI_API_KEY=your-key-here

# Build and deploy production
docker-compose -f docker-compose.python.yml --profile production up --build -d

# Or build individual containers
docker build -f python-backend/Dockerfile -t ai-chatbot-python ./python-backend
docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY ai-chatbot-python
```

## Performance & Scaling

- **Docker Multi-stage Builds**: Optimized production images
- **Virtual Environments**: Isolated Python dependencies
- **Volume Caching**: Persistent virtual environment storage
- **Health Checks**: Container health monitoring
- **Hot Reload**: Development efficiency
- **Streaming**: Reduces perceived latency with real-time responses

## Security Notes

- **Environment Isolation**: Docker containers provide security boundaries
- **Virtual Environments**: Dependency isolation
- **Secrets Management**: Environment variable injection
- **Network Isolation**: Docker network separation
- **Health Monitoring**: Container health checks

## Troubleshooting

### Common Issues

1. **Container Won't Start**: Check logs with `docker-compose logs`
2. **Debug Port Conflicts**: Change `DEBUG_PORT` in environment
3. **Volume Permission Issues**: On Linux, check Docker volume permissions
4. **Hot Reload Not Working**: Ensure volume mounts are correct
5. **OpenAI API Issues**: Check API key and quota

### Debug Commands

```bash
# Check container status
docker-compose -f docker-compose.python.yml ps

# View logs
docker-compose -f docker-compose.python.yml logs ai-chatbot-python-dev

# Access container shell
docker exec -it $(docker-compose -f docker-compose.python.yml ps -q ai-chatbot-python-dev) bash

# Check virtual environment
docker exec -it container_name which python
docker exec -it container_name pip list
```

## Development Tips

1. **Use VS Code Tasks**: Access common operations via Command Palette
2. **Monitor Logs**: Keep log window open during development
3. **Hot Reload**: Changes to Python files automatically restart server
4. **Breakpoint Debugging**: Set breakpoints and debug in containers
5. **Environment Variables**: Use `.env` files for local overrides

## Contributing

1. Fork the repository
2. Create a feature branch  
3. **Use Docker development environment**
4. Add tests for new features
5. Test with both mock and real OpenAI responses
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

---

**🐳 Quick Start**: `docker-compose -f docker-compose.python.yml --profile dev up --build`

**🔐 Demo Credentials**: Username: `admin`, Password: `admin123`

**🤖 AI Features**: Get your OpenAI API key at [platform.openai.com](https://platform.openai.com/api-keys)