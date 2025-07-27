#!/usr/bin/env python3
"""
Startup script for the AI Chatbot Python backend
"""
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"🚀 Starting AI Chatbot Python Backend")
    print(f"📍 Server: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🤖 OpenAI API: {'✅ Configured' if os.getenv('OPENAI_API_KEY') else '❌ Not configured (using mock)'}")
    
    # Start the server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if not debug else "debug"
    ) 