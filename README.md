# AI Chatbot Web Application

A modern, full-stack web application featuring an AI chatbot interface with database management capabilities. Built with React frontend and **dual backend support** - choose between **Node.js Express** or **Python FastAPI** backends, both with streaming responses and containerized with Docker for easy deployment.

## 🚀 **NEW: Dual Backend Architecture**

This application now features **two complete backend implementations**:

- **🟢 Node.js/Express Backend** - Original implementation with SQLite and OpenAI integration
- **🐍 Python FastAPI Backend** - Advanced implementation with OpenAI Agents SDK and streaming
- **⚙️ Configurable Frontend** - React client works seamlessly with either backend
- **🐳 Docker Support** - Complete containerization for both backend options

## Features

- 🔐 **User Authentication** - Secure login/registration system with JWT tokens
- 💬 **AI Chat Interface** - Interactive chatbot with **real-time streaming responses**  
- 🤖 **Dual AI Integration** - OpenAI GPT-4 support in both Node.js and Python backends
- 📊 **Data Management** - Real-time database table view with search and filtering
- 🎨 **Modern UI** - Commonwealth Bank inspired design with yellow and black
- 🐳 **Docker Ready** - Complete development and production containers for both backends
- 🔧 **Debug Support** - VS Code debugging with Docker containers
- 📱 **Mobile Friendly** - Responsive design for all device sizes
- ⚡ **Real-time Streaming** - Server-Sent Events for live AI responses
- 🔄 **Backend Flexibility** - Switch between Node.js and Python backends easily

## Architecture Options

### **Option 1: Node.js Backend (Original)**
- **Frontend**: React 18 with streaming support
- **Backend**: Node.js/Express with SQLite and OpenAI integration
- **Database**: SQLite for lightweight, embedded storage
- **Port**: 3001 (backend), 3000 (frontend dev)

### **Option 2: Python Backend (Advanced)**
- **Frontend**: React 18 with streaming support  
- **Backend**: Python FastAPI with OpenAI Agents SDK integration
- **AI**: Advanced OpenAI GPT-4 with Agents SDK
- **Database**: SQLite for lightweight, embedded storage
- **Port**: 8000 (backend), 3000 (frontend dev)

**Layout**: 80% data table view, 20% chat interface (responsive for both backends)

## Quick Start

### Prerequisites

- Docker and Docker Compose
- VS Code (recommended for debugging)
- OpenAI API Key (optional - uses mock responses without it)

### 🐳 **Option A: Docker Setup (Recommended)**

#### **Node.js Backend (Original)**

1. **Start Node.js Stack**
   ```bash
   git clone <your-repo-url>
   cd Banksie
   
   # Optional: Add your OpenAI API key
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   
   # Start Node.js backend stack
   docker-compose up --build
   ```

2. **Access Application**
   - **Full Application**: http://localhost:3001
   - **React Dev Server**: http://localhost:3000 (if running dev mode)

#### **Python Backend (Advanced)**

1. **Start Python Stack**
   ```bash
   git clone <your-repo-url>
   cd Banksie
   
   # Optional: Add your OpenAI API key  
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   
   # Start Python backend stack (development mode)
   docker-compose -f docker-compose.python.yml --profile dev up --build
   ```

2. **Access Application**
   - **React Frontend**: http://localhost:3000
   - **Python Backend**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Database Admin**: http://localhost:8080 (Adminer)

### 💻 **Option B: Local Development**

#### **Node.js Backend Setup**

1. **Install Dependencies**
   ```bash
   npm run install-all  # Installs root, server, and client dependencies
   ```

2. **Start Development**
   ```bash
   npm run dev  # Starts both server (3001) and client (3000)
   ```

#### **Python Backend Setup**

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
   REACT_APP_API_URL=http://localhost:8000 npm start
   ```

### 🔐 **Login Credentials**
- Username: `admin`
- Password: `admin123`

## 🐳 **Docker Development Features**

### **Node.js Docker Setup**
- **Single container** with both frontend build and backend
- **Production optimized** with multi-stage builds
- **Automatic restarts** with health checks
- **Volume mounting** for data persistence

### **Python Docker Setup** 
- **Virtual Environment** inside containers
- **VS Code Remote Debugging** support
- **Hot Reload** for both frontend and backend
- **Isolated Development** with proper dependency management

### **Available Profiles (Python)**
```bash
# Development mode (hot reload, debugging)
docker-compose -f docker-compose.python.yml --profile dev up

# Production mode (optimized builds)
docker-compose -f docker-compose.python.yml --profile production up
```

## 🔧 **VS Code Debugging**

### **Python Backend Debugging**

1. **Start Development Container**
   ```bash
   docker-compose -f docker-compose.python.yml --profile dev up -d
   ```

2. **Attach Debugger in VS Code**
   - Press `F5` → Select **"Debug Python Backend (Docker)"**
   - Set breakpoints in your Python code
   - Debug runs inside the Docker container!

### **Available Debug Configurations**:
- `Debug Python Backend (Local)` - Local Python debugging
- `Debug Python Backend (Docker)` - Remote Docker debugging  
- `Debug Python Backend (Docker - Wait)` - Wait for debugger attachment
- `Debug React Frontend` - React app debugging
- `Debug Full Stack (Docker)` - Both frontend and backend

## 🛠️ **Available VS Code Tasks**

Access via `Ctrl+Shift+P` → "Tasks: Run Task":

- **Start Full Stack (Docker Dev)** - Complete development environment
- **Start Python Backend Docker Dev** - Python backend only
- **Start Node.js Full Stack** - Node.js backend with frontend
- **Start React Frontend** - Frontend only
- **Stop Docker Services** - Stop all containers
- **View Docker Logs** - Monitor container logs
- **Run Tests (Python)** - Execute Python tests
- **Format Python Code** - Auto-format with Black

## **Project Structure**

```
ai-chatbot-webapp/
├── python-backend/              # 🐍 Python FastAPI backend
│   ├── main.py                 # FastAPI app with OpenAI Agents SDK
│   ├── start.py                # Standard startup script
│   ├── start-debug.py          # Debug startup with debugpy
│   ├── requirements.txt        # Production dependencies
│   ├── requirements.dev.txt    # Development dependencies
│   ├── Dockerfile              # Production container
│   ├── Dockerfile.dev          # Development container
│   └── ai_agents/              # OpenAI Agents implementation
├── server/                     # 🟢 Node.js Express backend
│   ├── index.js                # Express server with OpenAI integration
│   ├── package.json           # Node.js dependencies
│   └── database.sqlite        # SQLite database
├── client/                     # ⚛️ React frontend (works with both backends)
│   ├── src/components/         # React components with streaming
│   ├── src/setupProxy.js      # Proxy configuration for backend selection
│   ├── Dockerfile             # Production container  
│   ├── Dockerfile.dev         # Development container  
│   └── package.json           # Frontend dependencies
├── .vscode/                    # VS Code configuration
│   ├── launch.json            # Debug configurations
│   └── tasks.json             # Development tasks
├── docker-compose.yml          # 🟢 Node.js Docker setup
├── docker-compose.python.yml   # 🐍 Python Docker setup
├── Dockerfile                  # Root Dockerfile for Node.js stack
├── package.json               # Root package.json for Node.js orchestration
└── README.md
```

## 🤖 **AI Integration**

### **Setting up OpenAI API**

1. **Get API Key**: Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Set Environment Variable**:
   ```bash
   # Create .env file in project root
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   ```
3. **Without API Key**: Both backends use intelligent mock responses

### **Backend-Specific AI Features**

#### **Node.js Backend**
- **Direct OpenAI API** integration with GPT-4
- **Streaming responses** via Server-Sent Events
- **Context management** for conversation history
- **Rate limiting** and error handling

#### **Python Backend** 
- **OpenAI Agents SDK** for advanced AI capabilities
- **Contextual understanding** of data structure
- **Advanced streaming** with real-time message generation
- **Data analysis** capabilities for business intelligence

## **API Endpoints**

### **Common Endpoints (Both Backends)**
- `POST /api/login` - User login
- `POST /api/register` - User registration (Python only)
- `GET /api/data` - Fetch table data (authenticated)

### **Node.js Backend (Port 3001)**
- `GET /` - Serves complete application
- `POST /api/chat` - Send chat message
- `GET /api/chat/history` - Get chat history

### **Python Backend (Port 8000)**
- `GET /api/chat/history` - Get chat history (authenticated)
- `POST /api/chat/stream` - **Stream AI response** (Server-Sent Events)
- `WS /ws/chat/{user_id}` - WebSocket chat (alternative)
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger)

## **Environment Configuration**

### **Node.js Environment**
```env
# Server Configuration
NODE_ENV=development
PORT=3001
JWT_SECRET=your-jwt-secret-key
OPENAI_API_KEY=your-openai-api-key-here
```

### **Python Environment**
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

### **Frontend Configuration**
```env
# Backend Selection
REACT_APP_API_URL=http://localhost:8000  # Python backend
# REACT_APP_API_URL=http://localhost:3001  # Node.js backend
```

## **Development Workflow**

### **Typical Development Session**

#### **For Node.js Development**
```bash
# Start full stack
docker-compose up --build

# Or local development
npm run dev

# Access at http://localhost:3001 (production) or http://localhost:3000 (dev)
```

#### **For Python Development**
```bash
# Start development environment
docker-compose -f docker-compose.python.yml --profile dev up --build

# Start debugging in VS Code
# Press F5 → Select "Debug Full Stack (Docker)"

# Access at http://localhost:3000 (frontend) and http://localhost:8000 (backend)
```

## **Production Deployment**

### **Node.js Production**
```bash
# Build and deploy
docker-compose up --build -d

# Or build individual container
docker build -t ai-chatbot-node .
docker run -p 3001:3001 -e OPENAI_API_KEY=$OPENAI_API_KEY ai-chatbot-node
```

### **Python Production**
```bash
# Set your OpenAI API key
export OPENAI_API_KEY=your-key-here

# Build and deploy production
docker-compose -f docker-compose.python.yml --profile production up --build -d

# Or build individual container
docker build -f python-backend/Dockerfile -t ai-chatbot-python ./python-backend
docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY ai-chatbot-python
```

## **Performance & Scaling**

- **Docker Multi-stage Builds**: Optimized production images for both backends
- **Virtual Environments**: Isolated Python dependencies
- **Volume Caching**: Persistent dependency storage
- **Health Checks**: Container health monitoring for both stacks
- **Hot Reload**: Development efficiency
- **Streaming**: Reduces perceived latency with real-time responses
- **Backend Choice**: Choose optimal backend for your use case

## **Security Notes**

- **Environment Isolation**: Docker containers provide security boundaries
- **JWT Authentication**: Secure token-based authentication in both backends
- **Secrets Management**: Environment variable injection
- **Network Isolation**: Docker network separation
- **Health Monitoring**: Container health checks
- **Input Validation**: Request validation in both backends

## **Backend Comparison**

| Feature | Node.js Backend | Python Backend |
|---------|-----------------|----------------|
| **Language** | JavaScript/Node.js | Python |
| **Framework** | Express.js | FastAPI |
| **OpenAI Integration** | Direct API calls | OpenAI Agents SDK |
| **Performance** | Fast, lightweight | Feature-rich, advanced AI |
| **Development** | Simple setup | Advanced debugging |
| **Production Ready** | ✅ Yes | ✅ Yes |
| **Streaming** | Server-Sent Events | Server-Sent Events + WebSocket |
| **API Docs** | Manual | Auto-generated (Swagger) |
| **Best For** | Simple deployments | Advanced AI features |

## **Troubleshooting**

### **Common Issues**

1. **Wrong Backend Running**: Check which Docker compose file you're using
2. **Port Conflicts**: Node.js uses 3001, Python uses 8000
3. **Frontend Proxy Issues**: Check `REACT_APP_API_URL` environment variable
4. **Container Won't Start**: Check logs with `docker-compose logs`
5. **Debug Port Conflicts**: Change `DEBUG_PORT` in Python environment
6. **OpenAI API Issues**: Check API key and quota

### **Debug Commands**

```bash
# Check which containers are running
docker ps

# Node.js stack logs
docker-compose logs

# Python stack logs  
docker-compose -f docker-compose.python.yml logs

# Check frontend proxy configuration
cat client/src/setupProxy.js

# Test backend directly
curl http://localhost:3001/health  # Node.js
curl http://localhost:8000/health  # Python
```

## **Contributing**

1. Fork the repository
2. Create a feature branch
3. **Choose your backend** (Node.js or Python)
4. **Use appropriate Docker setup** for development
5. Add tests for new features
6. Test with both mock and real OpenAI responses
7. Submit a pull request

## **License**

MIT License - see LICENSE file for details.

---

## **Quick Reference**

### **🟢 Node.js Stack**
```bash
# Development
npm run dev

# Docker
docker-compose up --build

# Access: http://localhost:3001
```

### **🐍 Python Stack**  
```bash
# Development
docker-compose -f docker-compose.python.yml --profile dev up --build

# Access: http://localhost:3000 (frontend) + http://localhost:8000 (backend)
```

### **🔐 Demo Credentials**
- Username: `admin`  
- Password: `admin123`

### **🤖 AI Setup**
Get your OpenAI API key at [platform.openai.com](https://platform.openai.com/api-keys)