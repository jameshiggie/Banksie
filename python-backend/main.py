import json
import logging
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, List

import bcrypt
from ai_agents.banksie.banksie import BanksieAgent
from ai_agents.utils.state import StateContext
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

# Configure logging first (before loading environment variables)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from local .env file with priority order
# This ensures local .env files take precedence over global environment variables
def load_local_env():
    """
    Load environment variables from local .env file with multiple fallback locations.
    Priority order:
    1. .env in project root (one level up from python-backend/)
    2. .env in python-backend/ directory
    3. .env in current working directory
    """
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try different .env file locations in priority order
    env_locations = [
        # Project root (one level up from python-backend/)
        os.path.join(os.path.dirname(current_file_dir), '.env'),
        # python-backend directory
        os.path.join(current_file_dir, '.env'),
        # Current working directory
        os.path.join(os.getcwd(), '.env')
    ]
    
    env_loaded = False
    for env_path in env_locations:
        if os.path.exists(env_path):
            # Clear existing environment variables that might conflict
            # This ensures local .env takes precedence over global env vars
            load_dotenv(dotenv_path=env_path, override=True)
            logger.info(f"✓ Loaded environment variables from: {env_path}")
            env_loaded = True
            break
        else:
            logger.debug(f"✗ .env file not found at: {env_path}")
    
    if not env_loaded:
        logger.warning("⚠ No local .env file found. Using system environment variables.")
        # Still try to load from default locations as fallback
        load_dotenv(override=True)
    
    return env_loaded

# Load the local environment variables
load_local_env()

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

# Initialize AI Agent with proper error handling and logging
try:
    # Load OpenAI API key from project root .env file
    openai_key = os.getenv("OPENAI_API_KEY")
    
    # Debug information to help troubleshoot environment variable loading
    if openai_key:
        # Show first 10 and last 4 characters for debugging (keep middle hidden for security)
        masked_key = f"{openai_key[:10]}...{openai_key[-4:]}" if len(openai_key) > 14 else "***"
        logger.info(f"🔑 OpenAI API Key loaded: {masked_key}")
    else:
        logger.warning("❌ OpenAI API Key not found in environment variables")
        logger.warning("📋 Available environment variables starting with 'OPENAI':")
        for key, value in os.environ.items():
            if key.startswith('OPENAI'):
                masked_value = f"{value[:10]}...{value[-4:]}" if len(value) > 14 else "***"
                logger.warning(f"   {key}: {masked_value}")
    
    if not openai_key or not openai_key.strip() or openai_key == "your-openai-api-key-here":
        logger.error("OpenAI API key is missing or invalid. Please check your .env file.")
        logger.error("Expected format: OPENAI_API_KEY=sk-proj-your-actual-key-here")
        raise ValueError("Invalid or missing OpenAI API key")
    
    # Initialize the BanksieAgent
    ai_agent = BanksieAgent()
    logger.info("✓ Successfully initialized OpenAI-powered BanksieAgent")
    
except Exception as e:
    logger.error(f"❌ Failed to initialize BanksieAgent: {e}")
    logger.error("The chat functionality will not work without a valid OpenAI API key")
    logger.error("Please ensure your .env file contains: OPENAI_API_KEY=sk-proj-your-actual-key-here")
    ai_agent = None

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
            # Check if AI agent is properly initialized
            if ai_agent is None:
                logger.error("AI agent not initialized - cannot process chat request")
                yield f"data: {json.dumps({'error': True, 'message': 'AI service is not available. Please check server configuration.'})}\n\n"
                return
            
            # Create state context
            state_context = StateContext(prompt=chat_message.message)
            
            # Get streamed result from BanksieAgent
            result = await ai_agent.run(state_context, prompt=chat_message.message)
            
            # Check if result is valid
            if result is None:
                logger.error("AI agent returned None result")
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

@app.get("/health")
async def health_check():
    """Health check endpoint that reports AI agent availability"""
    ai_available = ai_agent is not None
    status = "healthy" if ai_available else "degraded"
    
    response = {
        "status": status,
        "ai_agent_available": ai_available,
        "timestamp": datetime.now().isoformat()
    }
    
    if not ai_available:
        response["message"] = "AI chat functionality is not available. Check OpenAI API key configuration."
        logger.warning("Health check: AI agent not available")
    
    return response

@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint to verify API connectivity"""
    return {"message": "API is working", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 