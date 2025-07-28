# Banksie GenAI Financial Analysis Backend

## Overview

Banksie is a business banking AI assistant built with **FastAPI** and the **OpenAI Agents SDK**. It provides intelligent 
financial analysis capabilities by allowing users to interact with their transaction data through natural language queries.
Banksie is a simple ReAct/CodeAct Manus like agent using the openai agents-sdk framework powered by gpt-4.1 API calls. 
The backend is written in Python and uses FastAPI to stream to the front end. 
The app is containerized within Docker and set up to run in debug mode in VS Code for development. 

[![Watch the video](https://img.youtube.com/vi/jE9jUqLCUuc/hqdefault.jpg)](https://www.youtube.com/watch?v=jE9jUqLCUuc)

### Usage Examples

```
"What are my top 5 expense categories this month?"
"Show me the variation, median and sum of sales in June 2025 and June 2024"
"give me some insights on what to focus on to improve"
"What's my average monthly revenue?"
"Which suppliers am I spending the most money with?"
"Calculate my total revenue for each month"
"Show me all transactions over $30,000 for aug 2024"
```

## Features

- 🔐 **User Authentication** - Secure login/registration system with JWT tokens
- 💬 **AI Chat Interface** - Interactive chatbot with **real-time streaming responses**  
- 🤖 **AI Integration** - OpenAI GPT-4 with Agents SDK for advanced capabilities
- 📊 **Data Management** - Real-time database table view with search and filtering
- 🎨 **Modern UI** - Commonwealth Bank inspired design with yellow and black
- 🐳 **Docker Ready** - Complete development and production containers
- 🔧 **Debug Support** - VS Code debugging with Docker containers
- 📱 **Mobile Friendly** - Responsive design for all device sizes
- ⚡ **Real-time Streaming** - Server-Sent Events for live AI responses

## Architecture

- **Frontend**: React 18 with streaming support  
- **Backend**: Python FastAPI with OpenAI Agents SDK integration
- **AI**: Advanced OpenAI GPT-4 with Agents SDK
- **Database**: SQLite for lightweight, embedded storage
- **Port**: 8000 (backend), 3000 (frontend dev)


## Quick Start

### Prerequisites

- Docker and Docker Compose
- VS Code (recommended for debugging)
- OpenAI API Key (optional - uses mock responses without it)

### 🐳 **Docker Setup (Recommended)**

1. **Start the Application**
   ```bash
   git clone <your-repo-url>
   cd Banksie
   
   # Optional: Add your OpenAI API key  
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   
   # Start development stack (hot reload, debugging)
   docker-compose -f docker-compose.python.yml --profile dev up --build
   ```

2. **Access Application**
   - **React Frontend**: http://localhost:3000
   - **Python Backend**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Database Admin**: http://localhost:8080 (Adminer)

### 💻 **Local Development**

1. **Setup Python Backend**
   ```bash
   cd app
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

- **Virtual Environment** inside containers
- **VS Code Remote Debugging** support
- **Hot Reload** for both frontend and backend
- **Isolated Development** with proper dependency management

### **Available Profiles**
```bash
# Development mode (hot reload, debugging)
docker-compose -f docker-compose.python.yml --profile dev up

# Production mode (optimized builds)
docker-compose -f docker-compose.python.yml --profile production up
```

## 🔧 **VS Code Debugging**

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
- **Start React Frontend** - Frontend only
- **Stop Docker Services** - Stop all containers
- **View Docker Logs** - Monitor container logs
- **Run Tests (Python)** - Execute Python tests
- **Format Python Code** - Auto-format with Black

## **Project Structure**

```
Banksie/
├── app/              # 🐍 Python FastAPI backend
│   ├── main.py                 # FastAPI app with OpenAI Agents SDK
│   ├── start.py                # Standard startup script
│   ├── start-debug.py          # Debug startup with debugpy
│   ├── requirements.txt        # Production dependencies
│   ├── requirements.dev.txt    # Development dependencies
│   ├── Dockerfile              # Production container
│   ├── Dockerfile.dev          # Development container
│   └── ai_agents/              # OpenAI Agents implementation
├── client/                     # ⚛️ React frontend
│   ├── src/components/         # React components with streaming
│   ├── src/setupProxy.js      # Proxy configuration
│   ├── Dockerfile             # Production container  
│   ├── Dockerfile.dev         # Development container  
│   └── package.json           # Frontend dependencies
├── .vscode/                    # VS Code configuration
│   ├── launch.json            # Debug configurations
│   └── tasks.json             # Development tasks
├── docker-compose.python.yml   # 🐍 Python Docker setup
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
3. **Without API Key**: The backend uses intelligent mock responses

### **AI Features**
- **OpenAI Agents SDK** for advanced AI capabilities
- **Contextual understanding** of data structure
- **Advanced streaming** with real-time message generation
- **Data analysis** capabilities for business intelligence

## **API Endpoints**

### **Authentication**
- `POST /api/login` - User login
- `POST /api/register` - User registration

### **Data & Chat**
- `GET /api/data` - Fetch table data (authenticated)
- `GET /api/chat/history` - Get chat history (authenticated)
- `POST /api/chat/stream` - **Stream AI response** (Server-Sent Events)
- `WS /ws/chat/{user_id}` - WebSocket chat (alternative)

### **System**
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger)

## **Environment Configuration**

### **Backend Environment**
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
# Backend URL
REACT_APP_API_URL=http://localhost:8000
```

## **Development Workflow**

### **Typical Development Session**

```bash
# Start development environment
docker-compose -f docker-compose.python.yml --profile dev up --build

# Start debugging in VS Code
# Press F5 → Select "Debug Full Stack (Docker)"

# Access at http://localhost:3000 (frontend) and http://localhost:8000 (backend)
```

## **Production Deployment**

```bash
# Set your OpenAI API key
export OPENAI_API_KEY=your-key-here

# Build and deploy production
docker-compose -f docker-compose.python.yml --profile production up --build -d

# Or build individual container
docker build -f app/Dockerfile -t ai-chatbot-python ./app
docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY ai-chatbot-python
```

## **Performance & Scaling**

- **Docker Multi-stage Builds**: Optimized production images
- **Virtual Environments**: Isolated Python dependencies
- **Volume Caching**: Persistent dependency storage
- **Health Checks**: Container health monitoring
- **Hot Reload**: Development efficiency
- **Streaming**: Reduces perceived latency with real-time responses

## **Security Notes**

- **Environment Isolation**: Docker containers provide security boundaries
- **JWT Authentication**: Secure token-based authentication
- **Secrets Management**: Environment variable injection
- **Network Isolation**: Docker network separation
- **Health Monitoring**: Container health checks
- **Input Validation**: Request validation

## **Troubleshooting**

### **Common Issues**

1. **Container Won't Start**: Check logs with `docker-compose -f docker-compose.python.yml logs`
2. **Debug Port Conflicts**: Change `DEBUG_PORT` in Python environment
3. **Frontend Proxy Issues**: Check `REACT_APP_API_URL` environment variable
4. **OpenAI API Issues**: Check API key and quota

### **Debug Commands**

```bash
# Check which containers are running
docker ps

# Check application logs  
docker-compose -f docker-compose.python.yml logs

# Check frontend proxy configuration
cat client/src/setupProxy.js

# Test backend directly
curl http://localhost:8000/health
```

## **Contributing**

1. Fork the repository
2. Create a feature branch
3. **Use Docker setup** for development
4. Add tests for new features
5. Test with both mock and real OpenAI responses
6. Submit a pull request

## **License**

MIT License - see LICENSE file for details.

---

## **Quick Reference**

### **🐍 Development Stack**  
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