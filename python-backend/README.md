# Banksie AI Financial Analysis Backend

## Overview

Banksie is a business banking AI assistant built with **FastAPI** and the **OpenAI Agents SDK**. It provides intelligent 
financial analysis capabilities by allowing users to interact with their transaction data through natural language queries.
Banksie is a simple ReAct/CodeAct Manus like agent using the openai agents-sdk framework powered by gpt4.1 API calls. 
The backend is written in python and uses FastAPI to stream to the front end. 
Frontend is Node.js, both front and back ends pull data that is stored in the same SQLite database. 
The app is containerized within docker and set up to run in debug mode in vscode for development. 

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

## Architecture

### 🏗️ **Core Components**

#### **FastAPI Backend** (`main.py`)
- **Authentication**: JWT-based user authentication with bcrypt password hashing
- **Database**: SQLite database with comprehensive transaction data generation
- **Real-time Chat**: Streaming chat API with Server-Sent Events (SSE)
- **CORS Support**: Configured for frontend integration
- **Health Monitoring**: Health check endpoints with AI agent status

#### **AI Agent System** (`ai_agents/`)
- **BanksieAgent**: Main agent orchestrator using OpenAI Agents SDK
- **Analyst Agent**: Specialized agent for financial data analysis
- **Code Execution Tool**: Dynamic Restricted Python code execution on transaction data
- **State Management**: Context-aware conversation handling

#### **Database Schema**
```sql
-- Users with authentication
users (id, username, password, email, created_at)

-- Business transactions with comprehensive data
transactions (id, transaction_date, description, category, 
             transaction_type, amount, balance, reference_number, 
             status, created_at)

-- Chat conversation history
chat_messages (id, user_id, message, response, created_at)
```

### **Agent Architecture**

#### **Analyst Agent** (`ai_agents/banksie/ai_agents/analyst.py`)
- **Model**: GPT-4.1 for advanced reasoning
- **Instructions**: Financial analysis specialist with banking terminology
- **Tool**: Single `perform_analysis` tool for code execution
- **Context**: Access to user's transaction data via StateContext


### **Data Flow**

1. **User Query** → FastAPI `/api/chat/stream` endpoint
2. **Authentication** → JWT token verification
3. **Data Loading** → Fetch user's transaction data from SQLite
4. **State Context** → Package data with user prompt
5. **Agent Execution** → BanksieAgent processes request
6. **Code Generation** → AI generates Python analysis code
7. **Execution** → Code runs in restricted environment with transaction data
8. **Streaming Response** → Results streamed back to frontend
9. **Database Storage** → Conversation saved to chat history

### **Transaction Data Structure**

```python
{
    "id": int,                    # Unique transaction ID
    "transaction_date": str,      # Date (YYYY-MM-DD)
    "description": str,           # Business entity/transaction description
    "category": str,              # Business category (Sales, Inventory, etc.)
    "transaction_type": str,      # 'Credit' or 'Debit'
    "amount": float,              # Transaction amount
    "balance": float,             # Running account balance
    "reference_number": str,      # Transaction reference
    "status": str,                # 'Completed' or 'Pending'
    "created_at": str            # Record timestamp
}
```

## Setup & Installation

### **Prerequisites**
- Python 3.11+
- OpenAI API key
- SQLite (included)

### **Local Development**

1. **Clone and Setup**
   ```bash
   cd python-backend
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   # Create .env file in project root or python-backend/
   echo "OPENAI_API_KEY=sk-proj-your-actual-key-here" > .env
   echo "JWT_SECRET=your-secret-key" >> .env
   echo "DEBUG=true" >> .env
   ```

3. **Run Development Server**
   ```bash
   python start.py
   # Or with debugging:
   python start-debug.py
   ```

4. **Access Application**
   - API: http://localhost:8000
   - Health Check: http://localhost:8000/health
   - API Docs: http://localhost:8000/docs

### **Docker Deployment**

#### **Development**
```bash
docker build -f Dockerfile.dev -t banksie-dev .
docker run -p 8000:8000 -p 5678:5678 \
  -e OPENAI_API_KEY=your-key \
  banksie-dev
```

#### **Production**
```bash
docker build -f Dockerfile -t banksie-prod .
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -e JWT_SECRET=your-secret \
  banksie-prod
```

## API Endpoints

### **Authentication**
- `POST /api/login` - User authentication
- `POST /api/register` - User registration

### **Data Access**
- `GET /api/data` - Fetch transaction data
- `GET /api/chat/history` - Get chat conversation history

### **AI Chat**
- `POST /api/chat/stream` - Streaming chat with financial analysis

### **Monitoring**
- `GET /health` - Application and AI agent health status
- `GET /api/test` - Simple API connectivity test


## **VS Code Docker Debug Setup**

For optimal development experience with breakpoints, variable inspection, and step-through debugging:

#### **1. Launch Configuration**
Create or update `.vscode/launch.json` in your project root:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Attach to Docker",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/python-backend",
                    "remoteRoot": "/app"
                }
            ],
            "justMyCode": false,
            "django": false,
            "subProcess": true
        },
        {
            "name": "Docker: Launch & Debug",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/python-backend/start-debug.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/python-backend",
                "DEBUG": "true",
                "DEBUG_WAIT": "true"
            },
            "cwd": "${workspaceFolder}/python-backend"
        }
    ]
}
```

#### **2. Docker Compose for Development**
Create `docker-compose.dev.yml` for easier debugging:

```yaml
version: '3.8'
services:
  banksie-backend:
    build:
      context: ./python-backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"  # FastAPI server
      - "5678:5678"  # Debug port
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - JWT_SECRET=${JWT_SECRET:-dev-secret-key}
      - DEBUG=true
      - DEBUG_WAIT=false
      - PYTHONPATH=/app
    volumes:
      - ./python-backend:/app
      - /app/__pycache__  # Exclude cache
    command: python start-debug.py
    stdin_open: true
    tty: true
```

#### **3. Debug Workflow**

**Option A: Automatic Attach (Recommended)**
```bash
# 1. Start container with debug server
docker-compose -f docker-compose.dev.yml up

# 2. In VS Code: F5 → Select "Python: Attach to Docker"
# 3. Set breakpoints and debug normally
```

**Option B: Wait for Debugger**
```bash
# 1. Set DEBUG_WAIT=true in docker-compose.dev.yml
# 2. Start container (will wait for debugger)
docker-compose -f docker-compose.dev.yml up

# 3. Container output shows: "⏳ Waiting for debugger to attach..."
# 4. In VS Code: F5 → Select "Python: Attach to Docker"
# 5. Container continues execution with debugger attached
```

**Option C: Local Debug (No Docker)**
```bash
# 1. In VS Code: F5 → Select "Docker: Launch & Debug" 
# 2. Runs locally with debugger attached from start
```

#### **4. Debug Features Available**

- **Breakpoints**: Set breakpoints in any Python file
- **Variable Inspection**: Hover over variables to see values
- **Call Stack**: Navigate through function calls
- **Watch Expressions**: Monitor specific variables/expressions
- **Step Through**: Step into, over, and out of functions
- **Console Access**: Execute Python code in debug context
- **Hot Reload**: Code changes reflected without restart (local mode)

#### **5. Environment Variables for Debug**

```bash
# .env file for debugging
OPENAI_API_KEY=sk-proj-your-actual-key-here
JWT_SECRET=debug-secret-key
DEBUG=true
DEBUG_PORT=5678
DEBUG_WAIT=false  # Set to true to wait for debugger
HOST=0.0.0.0
PORT=8000
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

## OpenAI Agents SDK Tracing for agent flow logs
OpenAI Agents SDK includes built-in tracing to log everything the agent does
 - LLM calls
 - Tool usage
 - Agent handoffs. 
 
Traces show up automatically in the OpenAI Platform so you can step through execution and debug issues.

## Future Enhancements

### **Potential Improvements**
- **Previous Message** add previous messages in the chat to the messages 
- **RAG/doc agent** add rag and doc agent to add domain knowledge to the core agents based of users business docs
- **Multi-agent Orchestration**: Specialized agents for different financial domains
- **Advanced Visualizations**: Chart and graph generation capabilities  
- **Export Functionality**: PDF reports and Excel spreadsheet generation
- **Scheduled Analysis**: Automated periodic financial reports
- **Integration APIs**: Connect with accounting software and bank APIs
- **Advanced Security**: Rate limiting, audit logging, and encryption at rest
- **Performance Optimization**: Caching layer and query optimization
- **Mobile Support**: Mobile-optimized API responses and push notifications
- **UI cuts of large wide tables**

This implementation provides a solid foundation for AI-powered financial analysis with room for extensive customization and feature expansion. 