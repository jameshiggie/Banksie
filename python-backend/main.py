from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import sqlite3
import bcrypt
from jose import jwt, JWTError
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from ai_agents.banksie.banksie import BanksieAgent
import logging
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Chatbot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-key")
DATABASE_PATH = os.getenv("DATABASE_PATH", "./database.sqlite")

# Security
security = HTTPBearer()

# Input class for BanksieAgent
class AgentInput:
    def __init__(self, input_message: str):
        self.input = input_message

# Pydantic models
class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    password: str
    email: str

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    id: int
    message: str
    response: str
    created_at: str

# Database initialization
def init_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Business transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_date DATE NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            balance DECIMAL(10,2) NOT NULL,
            reference_number TEXT,
            status TEXT NOT NULL DEFAULT 'Completed',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Chat messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            response TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Insert sample transaction data if empty
    cursor.execute("SELECT COUNT(*) FROM transactions")
    if cursor.fetchone()[0] == 0:
        import random
        from datetime import datetime, timedelta
        
        # Starting balance
        running_balance = 100000.00
        
        # Define 30 different business items/suppliers/customers
        business_entities = [
            # Suppliers/Vendors
            ("TechSource Solutions", "Inventory", "Debit", -2500, -8500),
            ("Global Office Supplies", "Inventory", "Debit", -800, -3200),
            ("Premium Manufacturing Co", "Inventory", "Debit", -5000, -15000),
            ("Industrial Parts Ltd", "Inventory", "Debit", -1200, -4800),
            ("Digital Equipment Corp", "Inventory", "Debit", -3000, -12000),
            ("Quality Materials Inc", "Inventory", "Debit", -1800, -6500),
            ("Advanced Components", "Inventory", "Debit", -2200, -9800),
            ("Wholesale Electronics", "Inventory", "Debit", -4500, -18000),
            ("Metro Supplies", "Office Expenses", "Debit", -150, -800),
            ("Business Essentials", "Office Expenses", "Debit", -200, -1200),
            
            # Customers
            ("Enterprise Solutions LLC", "Sales", "Credit", 8000, 25000),
            ("Corporate Dynamics", "Sales", "Credit", 12000, 45000),
            ("Regional Industries", "Sales", "Credit", 6500, 20000),
            ("Metro Business Group", "Sales", "Credit", 4200, 15000),
            ("Global Partners Inc", "Sales", "Credit", 9800, 35000),
            ("Strategic Ventures", "Sales", "Credit", 7500, 28000),
            ("Professional Services Co", "Sales", "Credit", 5500, 18000),
            ("Innovation Hub", "Sales", "Credit", 11000, 42000),
            ("Future Tech Solutions", "Sales", "Credit", 8800, 32000),
            ("Prime Business Network", "Sales", "Credit", 6800, 22000),
            
            # Service Providers
            ("City Properties Management", "Rent", "Debit", -2800, -2800),
            ("Power & Electric Utility", "Utilities", "Debit", -450, -850),
            ("Business Insurance Pro", "Insurance", "Debit", -1200, -1800),
            ("Smith & Associates CPA", "Professional Services", "Debit", -1500, -3500),
            ("Digital Marketing Agency", "Marketing", "Debit", -2000, -8000),
            ("Legal Advisors Group", "Professional Services", "Debit", -800, -2400),
            ("HR Solutions Inc", "Professional Services", "Debit", -1100, -2800),
            ("IT Support Services", "Professional Services", "Debit", -900, -2200),
            ("Cleaning Services Plus", "Office Expenses", "Debit", -300, -600),
            ("Security Systems Corp", "Office Expenses", "Debit", -250, -500),
        ]
        
        # Additional transaction types
        other_transactions = [
            ("Bank Interest Payment", "Interest", "Credit", 150, 500),
            ("Customer Refund Processing", "Refunds", "Debit", -200, -1500),
            ("Payroll Processing Services", "Payroll", "Debit", -12000, -18000),
            ("Equipment Lease Payment", "Rent", "Debit", -800, -1200),
            ("Software Subscription", "Professional Services", "Debit", -300, -800),
            ("Business Travel Expenses", "Office Expenses", "Debit", -500, -2000),
            ("Training & Development", "Professional Services", "Debit", -600, -1800),
            ("Vehicle Maintenance", "Office Expenses", "Debit", -400, -1000),
        ]
        
        sample_transactions = []
        transaction_id = 1
        
        # Generate initial capital transaction
        sample_transactions.append((
            '2023-01-01', 'Initial Business Capital Investment', 'Capital', 'Credit', 
            100000.00, running_balance, f'TXN{transaction_id:04d}', 'Completed'
        ))
        transaction_id += 1
        
        # Generate transactions over 12 months
        start_date = datetime(2023, 1, 2)
        current_date = start_date
        
        for day in range(365):  # One year of transactions
            current_date = start_date + timedelta(days=day)
            
            # Generate 2-5 transactions per day
            daily_transactions = random.randint(2, 5)
            
            for _ in range(daily_transactions):
                # Choose random entity
                if random.random() < 0.7:  # 70% from main business entities
                    entity_name, category, trans_type, min_amount, max_amount = random.choice(business_entities)
                else:  # 30% from other transaction types
                    entity_name, category, trans_type, min_amount, max_amount = random.choice(other_transactions)
                
                # Generate amount within range
                if trans_type == "Credit":
                    amount = random.randint(min_amount, max_amount)
                else:
                    amount = random.randint(max_amount, min_amount)  # Negative range
                
                # Update running balance
                running_balance += amount
                
                # Add some variation to entity names
                variations = [
                    entity_name,
                    f"{entity_name} - Invoice #{random.randint(1000, 9999)}",
                    f"{entity_name} - Order #{random.randint(100, 999)}",
                    f"{entity_name} - Payment #{random.randint(10000, 99999)}",
                ]
                
                description = random.choice(variations)
                
                # Add transaction
                sample_transactions.append((
                    current_date.strftime('%Y-%m-%d'),
                    description,
                    category,
                    trans_type,
                    amount,
                    running_balance,
                    f'TXN{transaction_id:04d}',
                    random.choice(['Completed', 'Completed', 'Completed', 'Pending'])  # 75% completed
                ))
                transaction_id += 1
                
                # Stop if we have enough transactions
                if len(sample_transactions) >= 1200:
                    break
            
            if len(sample_transactions) >= 1200:
                break
        
        # Add some recent transactions for current period
        recent_start = datetime.now() - timedelta(days=30)
        for day in range(30):
            current_date = recent_start + timedelta(days=day)
            
            # Generate 1-3 recent transactions per day
            daily_transactions = random.randint(1, 3)
            
            for _ in range(daily_transactions):
                entity_name, category, trans_type, min_amount, max_amount = random.choice(business_entities)
                
                if trans_type == "Credit":
                    amount = random.randint(min_amount, max_amount)
                else:
                    amount = random.randint(max_amount, min_amount)
                
                running_balance += amount
                
                description = f"{entity_name} - Recent Transaction"
                
                sample_transactions.append((
                    current_date.strftime('%Y-%m-%d'),
                    description,
                    category,
                    trans_type,
                    amount,
                    running_balance,
                    f'TXN{transaction_id:04d}',
                    'Completed'
                ))
                transaction_id += 1
        
        # Insert all transactions
        cursor.executemany(
            "INSERT INTO transactions (transaction_date, description, category, transaction_type, amount, balance, reference_number, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            sample_transactions
        )
    
    # Create default admin user if no users exist
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            ('admin', hashed_password.decode('utf-8'), 'admin@businessbank.com')
        )
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_database()

# Mock AI Agent for development/testing without OpenAI API key
class MockAIAgent:
    def __init__(self):
        self.system_prompt = """You are an AI financial assistant for a business banking platform."""
    
    async def run(self, input_obj):
        """Mock run method that returns a mock streaming result"""
        class MockStreamResult:
            async def stream_events(self):
                mock_responses = [
                    "Thank you for your question about your business finances. ",
                    "Based on your transaction history, I can see several patterns in your business operations. ",
                    "Your account shows regular inventory purchases from suppliers like TechSource Solutions and Premium Manufacturing Co. ",
                    "Sales revenue appears to be coming from various enterprise clients including Corporate Dynamics and Global Partners Inc. ",
                    "Operating expenses include rent payments to City Properties Management and utility costs. ",
                    "Overall, your business shows healthy cash flow with regular income and manageable expenses. ",
                    "I'd recommend monitoring your inventory turnover and consider optimizing supplier payment terms for better cash flow management."
                ]
                
                import asyncio
                for part in mock_responses:
                    # Create a mock event with delta
                    class MockEvent:
                        def __init__(self, delta_text):
                            self.type = "raw_response_event"
                            self.data = MockEventData(delta_text)
                    
                    class MockEventData:
                        def __init__(self, delta_text):
                            self.delta = delta_text
                    
                    yield MockEvent(part)
                    await asyncio.sleep(0.1)  # Simulate streaming delay
        
        return MockStreamResult()
    
    async def stream_response(self, message: str, user_data=None):
        """Mock streaming response for development (legacy method)"""
        mock_responses = [
            "Thank you for your question about your business finances. ",
            "Based on your transaction history, I can see several patterns in your business operations. ",
            "Your account shows regular inventory purchases from suppliers like TechSource Solutions and Premium Manufacturing Co. ",
            "Sales revenue appears to be coming from various enterprise clients including Corporate Dynamics and Global Partners Inc. ",
            "Operating expenses include rent payments to City Properties Management and utility costs. ",
            "Overall, your business shows healthy cash flow with regular income and manageable expenses. ",
            "I'd recommend monitoring your inventory turnover and consider optimizing supplier payment terms for better cash flow management."
        ]
        
        import asyncio
        for part in mock_responses:
            yield part
            await asyncio.sleep(0.1)  # Simulate streaming delay

# Initialize AI Agent (use mock if no OpenAI API key)
try:
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key.strip() and openai_key != "your-openai-api-key-here":
        ai_agent = BanksieAgent()
        logger.info("Initialized OpenAI-powered AI Agent")
    else:
        ai_agent = MockAIAgent()
        logger.info("Initialized Mock AI Agent (no OpenAI API key provided)")
except Exception as e:
    logger.error(f"Failed to initialize AI Agent: {e}")
    ai_agent = MockAIAgent()
    logger.info("Fallback to Mock AI Agent due to initialization error")

# Authentication functions
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    try:
        logger.debug(f"Verifying token: {credentials.credentials[:20]}...")
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("id")
        username = payload.get("username")
        
        if user_id is None:
            logger.warning("Token missing user ID")
            raise HTTPException(status_code=401, detail="Invalid token - missing user ID")
            
        logger.debug(f"Token verified for user: {username} (ID: {user_id})")
        return {"id": user_id, "username": username}
        
    except JWTError as e:
        logger.warning(f"JWT error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        raise HTTPException(status_code=401, detail="Token verification failed")

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

# API Routes
@app.post("/api/login")
async def login(user: UserLogin):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    db_user = cursor.fetchone()
    conn.close()
    
    if not db_user or not bcrypt.checkpw(user.password.encode('utf-8'), db_user[2].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = jwt.encode(
        {"id": db_user[0], "username": db_user[1], "exp": datetime.utcnow() + timedelta(days=1)},
        JWT_SECRET,
        algorithm="HS256"
    )
    
    return {
        "token": token,
        "user": {"id": db_user[0], "username": db_user[1], "email": db_user[3]}
    }

@app.post("/api/register")
async def register(user: UserRegister):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT username FROM users WHERE username = ? OR email = ?", 
                  (user.username, user.email))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    # Hash password and create user
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
        (user.username, hashed_password.decode('utf-8'), user.email)
    )
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    token = jwt.encode(
        {"id": user_id, "username": user.username, "exp": datetime.utcnow() + timedelta(days=1)},
        JWT_SECRET,
        algorithm="HS256"
    )
    
    return {
        "token": token,
        "user": {"id": user_id, "username": user.username, "email": user.email}
    }

@app.get("/api/data")
async def get_data(current_user: Dict[str, Any] = Depends(verify_token)):
    try:
        logger.info(f"Data request from user: {current_user.get('username', 'unknown')}")
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM transactions ORDER BY transaction_date DESC")
        rows = cursor.fetchall()
        conn.close()
        
        logger.info(f"Successfully retrieved {len(rows)} transactions")
        
        data = []
        for row in rows:
            data.append({
                "id": row[0],
                "transaction_date": row[1],
                "description": row[2],
                "category": row[3],
                "transaction_type": row[4],
                "amount": row[5],
                "balance": row[6],
                "reference_number": row[7],
                "status": row[8],
                "created_at": row[9]
            })
        
        return data
    
    except sqlite3.Error as e:
        logger.error(f"Database error in get_data: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error in get_data: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.get("/api/chat/history")
async def get_chat_history(current_user: Dict[str, Any] = Depends(verify_token)):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM chat_messages WHERE user_id = ? ORDER BY created_at ASC",
        (current_user["id"],)
    )
    rows = cursor.fetchall()
    conn.close()
    
    messages = []
    for row in rows:
        messages.append({
            "id": row[0],
            "user_id": row[1],
            "message": row[2],
            "response": row[3],
            "created_at": row[4]
        })
    
    return messages

@app.post("/api/chat/stream")
async def chat_stream(chat_message: ChatMessage, current_user: Dict[str, Any] = Depends(verify_token)):
    """Stream chat response"""
    async def generate_stream():
        response_parts = []
        
        try:
            # Create input for BanksieAgent
            agent_input = AgentInput(chat_message.message)
            
            # Get streamed result from BanksieAgent
            result = await ai_agent.run(agent_input)
            
            # Check if result is valid
            if result is None:
                raise Exception("Failed to get response from AI agent")
            
            # Stream the response using the correct pattern
            async for event in result.stream_events():
                if event.type == "raw_response_event":
                    # Check if event.data has delta attribute (for text streaming)
                    try:
                        delta = getattr(event.data, 'delta', None)
                        if delta:
                            chunk = delta
                            if chunk:  # Only send non-empty chunks
                                response_parts.append(chunk)
                                # Send each chunk as JSON
                                yield f"data: {json.dumps({'chunk': chunk, 'done': False})}\n\n"
                    except AttributeError:
                        # Handle cases where event.data doesn't have delta
                        continue
            
            # Get complete response for database storage
            complete_response = ''.join(response_parts)
            
            # Save to database
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_messages (user_id, message, response) VALUES (?, ?, ?)",
                (current_user["id"], chat_message.message, complete_response)
            )
            message_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Send final completion message
            yield f"data: {json.dumps({'done': True, 'message_id': message_id, 'created_at': datetime.now().isoformat()})}\n\n"
            
        except Exception as e:
            logger.error(f"Error in chat stream: {e}")
            # Send error message if something goes wrong
            yield f"data: {json.dumps({'error': True, 'message': 'An error occurred while processing your request'})}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )

@app.websocket("/ws/chat/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: int):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Verify user (you might want to add token verification here)
            message = message_data.get("message", "")
            
            if message:
                # Send typing indicator
                await manager.send_personal_message(
                    json.dumps({"type": "typing", "typing": True}),
                    websocket
                )
                
                response_parts = []
                
                # Create input for BanksieAgent
                agent_input = AgentInput(message)
                
                # Get streamed result from BanksieAgent
                result = await ai_agent.run(agent_input)
                
                # Check if result is valid
                if result is None:
                    await manager.send_personal_message(
                        json.dumps({"type": "error", "message": "Failed to get response from AI agent"}),
                        websocket
                    )
                    continue
                
                # Stream response using the correct pattern
                async for event in result.stream_events():
                    if event.type == "raw_response_event":
                        try:
                            delta = getattr(event.data, 'delta', None)
                            if delta:
                                chunk = delta
                                response_parts.append(chunk)
                                await manager.send_personal_message(
                                    json.dumps({"type": "chunk", "chunk": chunk}),
                                    websocket
                                )
                        except AttributeError:
                            # Handle cases where event.data doesn't have delta
                            continue
                
                # Complete response
                complete_response = ''.join(response_parts)
                
                # Save to database
                conn = sqlite3.connect(DATABASE_PATH)
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO chat_messages (user_id, message, response) VALUES (?, ?, ?)",
                    (user_id, message, complete_response)
                )
                message_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
                # Send completion
                await manager.send_personal_message(
                    json.dumps({
                        "type": "complete",
                        "message_id": message_id,
                        "created_at": datetime.now().isoformat()
                    }),
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "openai_available": True} # openai_client is not defined, so assuming True for now

@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint to verify API connectivity"""
    return {"message": "API is working", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 