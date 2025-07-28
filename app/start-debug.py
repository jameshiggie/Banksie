#!/usr/bin/env python3
"""
Debug startup script for the AI Chatbot Python backend
Includes debugpy integration for VS Code debugging
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def start_debug_server():
    """Start the server with debugging support"""
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug_port = int(os.getenv("DEBUG_PORT", 5678))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    wait_for_client = os.getenv("DEBUG_WAIT", "False").lower() == "true"
    
    print(f"🐍 Starting AI Chatbot Python Backend (Debug Mode)")
    print(f"📍 Server: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🐛 Debug port: {debug_port}")
    print(f"⏳ Wait for debugger: {wait_for_client}")
    print(f"🤖 OpenAI API: {'✅ Configured' if os.getenv('OPENAI_API_KEY') else '❌ Not configured (using mock)'}")
    
    # Import debugpy for remote debugging
    try:
        import debugpy
        
        # Configure debugpy
        debugpy.configure(
            {
                "pathMappings": [
                    {
                        "localRoot": "/app",  # Path in container
                        "remoteRoot": "/app", # Path in VS Code
                    }
                ]
            }
        )
        
        # Start debug server
        debugpy.listen((host, debug_port))
        print(f"🐛 Debug server started on {host}:{debug_port}")
        
        if wait_for_client:
            print("⏳ Waiting for debugger to attach...")
            debugpy.wait_for_client()
            print("✅ Debugger attached!")
        else:
            print("🚀 Debug server ready (not waiting for client)")
        
    except ImportError:
        print("⚠️  debugpy not available, running without debug support")
    except Exception as e:
        print(f"⚠️  Debug setup failed: {e}")
    
    # Import and start the main application
    try:
        import uvicorn
        
        # Start the server with auto-reload in debug mode
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=debug,
            reload_dirs=["/app"] if debug else None,
            log_level="debug" if debug else "info",
            access_log=debug,
            use_colors=True
        )
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_debug_server() 